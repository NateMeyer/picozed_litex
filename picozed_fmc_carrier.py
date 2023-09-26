#!/usr/bin/env python3

#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2023 Nate Meyer <nate.devel@gmail.com>
# SPDX-License-Identifier: BSD-2-Clause


from migen import *

from litex.gen import *

import picozed_z7030
from litex.build.tools import write_to_file
from litex.build.openocd import OpenOCD

from litex.soc.interconnect import axi
from litex.soc.interconnect import wishbone

from litex.soc.cores.clock import *
from litex.soc.integration.soc_core import *
from litex.soc.integration.soc import SoCRegion
from litex.soc.integration.builder import *
from litex.soc.cores.led import LedChaser

from litepcie.phy.s7pciephy import S7PCIEPHY
from litepcie.core import LitePCIeEndpoint, LitePCIeMSI
from litepcie.frontend.dma import LitePCIeDMA
from litepcie.frontend.wishbone import LitePCIeWishboneBridge
from litepcie.software import generate_litepcie_software

# CRG ----------------------------------------------------------------------------------------------


class _CRG(LiteXModule):
    def __init__(self, platform, sys_clk_freq, use_ps7_clk=False):
        self.rst    = Signal()
        self.cd_sys = ClockDomain()

        if use_ps7_clk:
            self.comb += ClockSignal("sys").eq(ClockSignal("ps7"))
            self.comb += ResetSignal("sys").eq(ResetSignal("ps7") | self.rst)
        else:
            # Clk.
            clk100 = platform.request("clk_pl")

            # PLL.
            self.pll = pll = S7PLL(speedgrade=-1)
            self.comb += pll.reset.eq(self.rst)
            pll.register_clkin(clk100, 100e6)
            pll.create_clkout(self.cd_sys, sys_clk_freq)
            # Ignore sys_clk to pll.clkin path created by SoC's rst.
            platform.add_false_path_constraints(self.cd_sys.clk, pll.clkin)

# BaseSoC ------------------------------------------------------------------------------------------


class BaseSoC(SoCCore):
    def __init__(self, toolchain="vivado", sys_clk_freq=125e6, with_led_chaser = True, with_pcie=True,
            **kwargs):
        platform = picozed_z7030.Platform(toolchain=toolchain)

        # CRG --------------------------------------------------------------------------------------
        use_ps7_clk = (kwargs.get("cpu_type", None) == "zynq7000")
        self.crg = _CRG(platform, sys_clk_freq, use_ps7_clk)

        # SoCCore ----------------------------------------------------------------------------------
        if kwargs.get("cpu_type", None) == "zynq7000":
            kwargs["integrated_sram_size"] = 0
            kwargs["with_uart"]            = False
            self.mem_map = { 
                'csr': 0x4000_0000,  # Zynq GP0 default
            }
        SoCCore.__init__(self, platform, sys_clk_freq, ident="LiteX SoC on Picozed Z7", **kwargs)

       
        # Zynq7000 Integration ---------------------------------------------------------------------
        if kwargs.get("cpu_type", None) == "zynq7000":
            assert toolchain == "vivado", ' not tested / specific vivado cmds'

            self.cpu.set_ps7(name="Zynq",
                config={
                    **platform.ps7_config,
                    "PCW_FPGA0_PERIPHERAL_FREQMHZ" : sys_clk_freq / 1e6,
                })

            # Connect AXI GP0 to the SoC
            wb_gp0 = wishbone.Interface()
            self.submodules += axi.AXI2Wishbone(
                axi          = self.cpu.add_axi_gp_master(),
                wishbone     = wb_gp0,
                base_address = self.mem_map["csr"])
            self.bus.add_master(master=wb_gp0)

            self.bus.add_region("sram", SoCRegion(
                origin = self.cpu.mem_map["sram"],
                size   = 512 * 1024 * 1024 - self.cpu.mem_map["sram"])
            )
            self.bus.add_region("rom", SoCRegion(
                origin = self.cpu.mem_map["rom"],
                size   = 256 * 1024 * 1024 // 8,
                linker = True)
            )

        # Leds -------------------------------------------------------------------------------------
        if with_led_chaser:
            self.leds = LedChaser(
                pads         = platform.request_all("user_led"),
                sys_clk_freq = sys_clk_freq)
            
        # PCIe -------------------------------------------------------------------------------------
        if with_pcie:
            # PHY
            self.pcie_phy = S7PCIEPHY(platform, platform.request(f"pcie_x1"),
                data_width = 64,
                bar0_size  = 0x20000,
            )
            self.pcie_phy.add_ltssm_tracer()

            self.add_pcie(phy=self.pcie_phy, ndmas=1, dma_buffering_depth=1024, max_pending_requests=4)

            # # ICAP (For FPGA reload over PCIe).
            # from litex.soc.cores.icap import ICAP
            # self.icap = ICAP()
            # self.icap.add_reload()
            # self.icap.add_timing_constraints(platform, sys_clk_freq, self.crg.cd_sys.clk)
        
        # UARTBone ---------------------------------------------------------------------------------
        platform.add_extension(picozed_z7030.uart_pmod_io("pmodz"))
        self.add_uartbone(uart_name="pl_serial")

    def finalize(self, *args, **kwargs):
        super(BaseSoC, self).finalize(*args, **kwargs)
        if self.cpu_type != "zynq7000":
            return

        libxil_path = os.path.join(self.builder.software_dir, 'libxil')
        os.makedirs(os.path.realpath(libxil_path), exist_ok=True)
        lib = os.path.join(libxil_path, 'embeddedsw')
        if not os.path.exists(lib):
            os.system(f"git clone --depth 1 --branch xilinx_v2023.1 https://github.com/Xilinx/embeddedsw {lib}")

        os.makedirs(os.path.realpath(self.builder.include_dir), exist_ok=True)
        for header in [
            'XilinxProcessorIPLib/drivers/uartps/src/xuartps_hw.h',
            'lib/bsp/standalone/src/common/xil_types.h',
            'lib/bsp/standalone/src/common/xil_assert.h',
            'lib/bsp/standalone/src/common/xil_io.h',
            'lib/bsp/standalone/src/common/xil_printf.h',
            'lib/bsp/standalone/src/common/xstatus.h',
            'lib/bsp/standalone/src/common/xdebug.h',
            'lib/bsp/standalone/src/arm/cortexa9/xpseudo_asm.h',
            'lib/bsp/standalone/src/arm/cortexa9/xreg_cortexa9.h',
            'lib/bsp/standalone/src/arm/cortexa9/xil_cache.h',
            'lib/bsp/standalone/src/arm/cortexa9/xparameters_ps.h',
            'lib/bsp/standalone/src/arm/cortexa9/xil_errata.h',
            'lib/bsp/standalone/src/arm/cortexa9/xtime_l.h',
            'lib/bsp/standalone/src/arm/common/xil_exception.h',
            'lib/bsp/standalone/src/arm/common/gcc/xpseudo_asm_gcc.h',
        ]:
            shutil.copy(os.path.join(lib, header), self.builder.include_dir)
        write_to_file(os.path.join(self.builder.include_dir, 'bspconfig.h'),
                      '#define FPU_HARD_FLOAT_ABI_ENABLED 1')
        write_to_file(os.path.join(self.builder.include_dir, 'xparameters.h'), '''
#ifndef __XPARAMETERS_H
#define __XPARAMETERS_H

#include "xparameters_ps.h"

#define STDOUT_BASEADDRESS 0xE0000000
#define XPAR_PS7_DDR_0_S_AXI_BASEADDR 0x00100000
#define XPAR_PS7_DDR_0_S_AXI_HIGHADDR 0x1FFFFFFF

#endif
''')


# Build --------------------------------------------------------------------------------------------


def main():
    from litex.build.parser import LiteXArgumentParser
    parser = LiteXArgumentParser(platform=picozed_z7030.Platform, description="LiteX SoC on Picozed z7030")
    parser.add_target_argument("--sys-clk-freq", default=125e6, type=float, help="System clock frequency.")
    parser.add_argument("--driver", action="store_true", help="Generate LitePCIe driver")
    parser.set_defaults(cpu_type="zynq7000")
    parser.set_defaults(soc_csv="csr.csv")
    parser.set_defaults(with_pcie=True)
    args = parser.parse_args()

    soc = BaseSoC(
        toolchain    = args.toolchain,
        sys_clk_freq = args.sys_clk_freq,
        **parser.soc_argdict
    )
    builder = Builder(soc, **parser.builder_argdict)
    if args.cpu_type == "zynq7000":
        soc.builder = builder
        builder.add_software_package('libxil')
        builder.add_software_library('libxil')

    if args.build:
        builder.build(**parser.toolchain_argdict)

    if args.driver:
        generate_litepcie_software(soc, os.path.join(builder.output_dir, "driver"))

    if args.load:
        prog = OpenOCD(config="scripts/picozed-tigard.cfg")
        prog.load_bitstream(builder.get_bitstream_filename(mode="sram"))

if __name__ == "__main__":
    main()
