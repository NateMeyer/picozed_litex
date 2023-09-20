# This file is Copyright (c) 2019 Michael Betz <michibetz@gmail.com>
# License: BSD

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
        Subsignal("rx_n",       Pins("AB7")),
        Subsignal("rx_p",       Pins("AA7")),
        Subsignal("tx_n",       Pins("AB3")),
        Subsignal("tx_p",       Pins("AA3")),
        Subsignal("rst_n",      Pins("V13"), IOStandard("LVCMOS33")),
        Subsignal("clk_n",      Pins("V9")),
        Subsignal("clk_p",      Pins("U9")),
    ),

    # PS7
    ("ps7_clk",   0, Pins(1)),
    ("ps7_porb",  0, Pins(1)),
    ("ps7_srstb", 0, Pins(1)),
    ("ps7_mio",   0, Pins(54)),
    ("ps7_ddram", 0,
        Subsignal("addr",    Pins(15)),
        Subsignal("ba",      Pins(3)),
        Subsignal("cas_n",   Pins(1)),
        Subsignal("ck_n",    Pins(1)),
        Subsignal("ck_p",    Pins(1)),
        Subsignal("cke",     Pins(1)),
        Subsignal("cs_n",    Pins(1)),
        Subsignal("dm",      Pins(4)),
        Subsignal("dq",      Pins(32)),
        Subsignal("dqs_n",   Pins(4)),
        Subsignal("dqs_p",   Pins(4)),
        Subsignal("odt",     Pins(1)),
        Subsignal("ras_n",   Pins(1)),
        Subsignal("reset_n", Pins(1)),
        Subsignal("we_n",    Pins(1)),
        Subsignal("vrn",     Pins(1)),
        Subsignal("vrp",     Pins(1)),

    ),
]

# Connectors ---------------------------------------------------------------------------------------

_connectors = [
    # access a pin with `pmoda:N`, where N is:
    #   N: 0  1  2  3  4  5  6  7
    # Pin: 1  2  3  4  7  8  9 10
    # Bank 13
    # ("pmoda", "Y18 Y19 Y16 Y17 U18 U19 W18 W19"),
    # ("pmodb", "W14 Y14 T11 T10 V16 W16 V12 W13"),
    
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

# PS7 config ---------------------------------------------------------------------------------------

ps7_config = {
    "PCW_PRESET_BANK1_VOLTAGE"           : "LVCMOS 1.8V",
    "PCW_CRYSTAL_PERIPHERAL_FREQMHZ"     : "33",
    "PCW_APU_PERIPHERAL_FREQMHZ"         : "650",
    "PCW_SDIO_PERIPHERAL_FREQMHZ"        : "50",
    "PCW_FPGA0_PERIPHERAL_FREQMHZ"       : "100",
    "PCW_UIPARAM_DDR_FREQ_MHZ"           : "525",
    "PCW_UIPARAM_DDR_BUS_WIDTH"          : "32 Bit",
    "PCW_UIPARAM_DDR_PARTNO"             : "MT41K256M16 RE-125",
    "PCW_UIPARAM_DDR_DQS_TO_CLK_DELAY_0" : "0.040",
    "PCW_UIPARAM_DDR_DQS_TO_CLK_DELAY_1" : "0.058",
    "PCW_UIPARAM_DDR_DQS_TO_CLK_DELAY_2" : "-0.009",
    "PCW_UIPARAM_DDR_DQS_TO_CLK_DELAY_3" : "-0.033",
    "PCW_UIPARAM_DDR_BOARD_DELAY0"       : "0.223",
    "PCW_UIPARAM_DDR_BOARD_DELAY1"       : "0.212",
    "PCW_UIPARAM_DDR_BOARD_DELAY2"       : "0.085",
    "PCW_UIPARAM_DDR_BOARD_DELAY3"       : "0.092",
    "PCW_QSPI_PERIPHERAL_ENABLE"         : "1",
    "PCW_QSPI_GRP_SINGLE_SS_ENABLE"      : "1",
    "PCW_QSPI_GRP_FBCLK_ENABLE"          : "1",
    "PCW_ENET0_PERIPHERAL_ENABLE"        : "0",
    "PCW_ENET0_ENET0_IO"                 : "MIO 16 .. 27",
    "PCW_ENET0_GRP_MDIO_ENABLE"          : "1",
    "PCW_ENET0_GRP_MDIO_IO"              : "MIO 52 .. 53",
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
