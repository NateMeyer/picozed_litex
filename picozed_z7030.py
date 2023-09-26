# Copyright (c) 2023 Nate Meyer <nate.devel@gmail.com>
# SPDX-License-Identifier: BSD-2-Clause

from litex.build.generic_platform import Pins, IOStandard, Subsignal
from litex.build.xilinx import Xilinx7SeriesPlatform

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Clk / Rst
    ("clk_pl", 0, Pins("Y18"), IOStandard("LVCMOS18")),

    # Leds
    ("user_led", 0, Pins("G3"), IOStandard("LVCMOS18")),
    ("user_led", 1, Pins("AA19"), IOStandard("LVCMOS33")),
    ("user_led", 2, Pins("AA20"), IOStandard("LVCMOS33")),
    ("user_led", 3, Pins("AB21"), IOStandard("LVCMOS33")),

    # Buttons
    # ("user_btn", 0, Pins("D19"), IOStandard("LVCMOS18")),
    # ("user_btn", 1, Pins("D20"), IOStandard("LVCMOS18")),
    # ("user_btn", 2, Pins("L20"), IOStandard("LVCMOS18")),
    # ("user_btn", 3, Pins("L19"), IOStandard("LVCMOS18")),

	# SPI
    # ("spi", 0,
    #     Subsignal("clk",  Pins("H15")),
    #     Subsignal("cs_n", Pins("F16")),
    #     Subsignal("mosi", Pins("T12")),
    #     Subsignal("miso", Pins("W15")),
    #     IOStandard("LVCMOS33"),
    # ),


    # PCIE
    ("pcie_x1", 0,
        Subsignal("rst_n",      Pins("V13"), IOStandard("LVCMOS33")),
        Subsignal("rx_p",       Pins("AA7")),
        Subsignal("rx_n",       Pins("AB7")),
        Subsignal("tx_p",       Pins("AA3")),
        Subsignal("tx_n",       Pins("AB3")),
        Subsignal("clk_p",      Pins("U9")),
        Subsignal("clk_n",      Pins("V9")),
    ),
    
    # PS7
    ("ps7_clk",   0, Pins("F16")),
    ("ps7_porb",  0, Pins("B18")),
    ("ps7_srstb", 0, Pins("C14")),
    ("ps7_mio",   0, Pins(
        "G17 A22 A21 F17 E19 A20 A19 D18 E18 C19",
        "G16 B19 C18 A17 B17 E17 D17 E14 A16 E13",
        "A15 F12 A9 E12 B16 F11 A10 D16 A11 E15",
        "A12 F14 C16 G11 B11 F9 A14 B9 F10 C10",
        "E9 C15 D15 B12 E10 B14 D11 B13 D12 C9",
        "D10 C13 D13 C11"
        )),
    ("ps7_ddram", 0,
        Subsignal("addr", Pins(
            "M19 M18 K19 L19 K17 K18 J16" ,
            "J17 J18 H18 J20 G18 H19 F19 G19" 
            )),
        Subsignal("ba",    Pins("L16 L17 M17")),
        Subsignal("cas_n", Pins("P20")),
        Subsignal("cke",   Pins("T19")),
        Subsignal("ck_n",  Pins("N18")),
        Subsignal("ck_p",  Pins("N19")),
        Subsignal("cs_n",  Pins("P17")),
        Subsignal("dm",    Pins("B22 H20 P22 AA21")),
        Subsignal("dq", Pins(
            "D22 C20 B21 D20 E20 E22 F21 F22 ",
            "G21 G22 L22 L21 L20 K22 J22 K20 ",
            "M22 T20 N20 T22 R20 T21 M21 R22 ",
            "Y20 U22 AA22 U21 W22 W20 V20 Y22")),
        Subsignal("dqs_n",   Pins("D21 J21 P21 W21")),
        Subsignal("dqs_p",   Pins("C21 H21 N21 V21")),
        Subsignal("reset_n", Pins("F20")),
        Subsignal("odt",     Pins("P18")),
        Subsignal("ras_n",   Pins("R18")),
        Subsignal("vrn",     Pins("M16")),
        Subsignal("vrp",     Pins("N16")),
        Subsignal("we_n",    Pins("R19"))
    ),
]

# Connectors ---------------------------------------------------------------------------------------

_connectors = [
    # access a pin with `pmoda:N`, where N is:
    #   N: 0  1  2  3  4  5  6  7
    # Pin: 1  2  3  4  7  8  9 10
    # Bank 13
    ("pmoda", "AA14 AA15 Y14 Y15 U19 V19 V18 W18"),
    ("pmodb", "AA16 AA17 AA11 AB11 Y12 Y13 V11 W11"),
    ("pmodz", "R17 T17 W12 W13 V16 W16 V15 W15")
    
    # ("XADC", {
        # Outer Analog Header
        # "vaux1_p"  : "E17",
        # "vaux1_n"  : "B18",
        # "vaux9_p"  : "E18",
        # "vaux9_n"  : "E19",
        # "vaux6_p"  : "K14",
        # "vaux6_n"  : "J14",
        # "vaux15_p" : "K16",
        # "vaux15_n" : "J16",
        # "vaux5_p"  : "J20",
        # "vaux5_n"  : "H20",
        # "vaux13_p" : "G19",
        # "vaux13_n" : "G20",

        # Inner Analog Header
        # "vaux12_p" : "F19",
        # "vaux12_n" : "F20",
        # "vaux0_p"  : "C20",
        # "vaux0_n"  : "B20",
        # "vaux8_p"  : "B19",
        # "vaux8_n"  : "A19",
    # })
]

def uart_pmod_io(pmod):
    return [
        ("pl_serial", 0,
            Subsignal("tx", Pins(f"{pmod}:1")),
            Subsignal("rx", Pins(f"{pmod}:2")),
            IOStandard("LVCMOS33")
        ),
    ]

# PS7 config ---------------------------------------------------------------------------------------

ps7_config = {
    "PCW_PRESET_BANK1_VOLTAGE"           : "LVCMOS 1.8V",
    "PCW_CRYSTAL_PERIPHERAL_FREQMHZ"     : "33.333333",
    "PCW_APU_PERIPHERAL_FREQMHZ"         : "667",
    "PCW_SDIO_PERIPHERAL_FREQMHZ"        : "50",
    "PCW_FPGA0_PERIPHERAL_FREQMHZ"       : "100",
    "PCW_UIPARAM_DDR_FREQ_MHZ"           : "533.333333",
    "PCW_UIPARAM_DDR_BUS_WIDTH"          : "32 Bit",
    "PCW_UIPARAM_DDR_PARTNO"             : "MT41K256M16 RE-125",
    "PCW_UIPARAM_DDR_DQS_TO_CLK_DELAY_0" : "-0.036",
    "PCW_UIPARAM_DDR_DQS_TO_CLK_DELAY_1" : "-0.036",
    "PCW_UIPARAM_DDR_DQS_TO_CLK_DELAY_2" : "0.058",
    "PCW_UIPARAM_DDR_DQS_TO_CLK_DELAY_3" : "0.057",
    "PCW_UIPARAM_DDR_BOARD_DELAY0"       : "0.240",
    "PCW_UIPARAM_DDR_BOARD_DELAY1"       : "0.238",
    "PCW_UIPARAM_DDR_BOARD_DELAY2"       : "0.283",
    "PCW_UIPARAM_DDR_BOARD_DELAY3"       : "0.284",
    "PCW_QSPI_PERIPHERAL_ENABLE"         : "1",
    "PCW_QSPI_GRP_SINGLE_SS_ENABLE"      : "1",
    "PCW_QSPI_GRP_FBCLK_ENABLE"          : "1",
    "PCW_ENET0_PERIPHERAL_ENABLE"        : "1",
    "PCW_ENET0_ENET0_IO"                 : "MIO 16 .. 27",
    "PCW_ENET0_GRP_MDIO_ENABLE"          : "1",
    "PCW_ENET0_GRP_MDIO_IO"              : "MIO 52 .. 53",
    "PCW_ENET0_PERIPHERAL_CLKSRC"        : "IO PLL",
    "PCW_ENET0_PERIPHERAL_DIVISOR0"      : "8",
    "PCW_ENET0_PERIPHERAL_DIVISOR1"      : "1",
    "PCW_ENET0_PERIPHERAL_ENABLE"        : "1",
    "PCW_ENET0_PERIPHERAL_FREQMHZ"       : "1000 Mbps",
    "PCW_ENET0_RESET_ENABLE"             : "0",
    "PCW_UART0_PERIPHERAL_ENABLE"        : "1",
    "PCW_UART0_UART0_IO"                 : "MIO 48 .. 49",
    "PCW_USB0_PERIPHERAL_ENABLE"         : "1",
    "PCW_USB0_RESET_ENABLE"              : "1",
    "PCW_USB0_RESET_IO"                  : "MIO 7",
    "PCW_GPIO_MIO_GPIO_ENABLE"           : "1",
    "PCW_GPIO_MIO_GPIO_IO"               : "MIO",
    "PCW_GPIO_EMIO_GPIO_ENABLE"          : "0",
}

# Platform -----------------------------------------------------------------------------------------

class Platform(Xilinx7SeriesPlatform):
    default_clk_name   = "clk_pl"
    default_clk_period = 1e9/100e6

    def __init__(self, toolchain="vivado"):
        device = "xc7z030sbg485-1"
        self.board = "picozed_z7_30"

        Xilinx7SeriesPlatform.__init__(self, device, _io, _connectors, toolchain=toolchain)
        self.ps7_config = ps7_config
        self.add_platform_command("set_property IOSTANDARD LVCMOS18 [get_ports -of_objects [get_iobanks 34]]")
        self.add_platform_command("set_property IOSTANDARD LVCMOS18 [get_ports -of_objects [get_iobanks 35]]")
        self.add_platform_command("set_property IOSTANDARD LVCMOS33 [get_ports -of_objects [get_iobanks 13]]")
        self.toolchain.bitstream_commands = ["set_property BITSTREAM.GENERAL.COMPRESS TRUE [current_design]", ]

    def do_finalize(self, fragment):
        Xilinx7SeriesPlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk_pl", loose=True), 1e9/100e6)
