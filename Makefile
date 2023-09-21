litex_platform = picozed_z7030
uboot_device_tree = zynq-picozed
uboot_defconfig = xilinx_zynq_virt_defconfig

soc_dir = build/$(litex_platform)
uboot_build_dir = $(soc_dir)/software/u-boot
uboot_src_dir = ext_src/u-boot
soc = ./picozed_fmc_carrier.py
bitstream_file = $(soc_dir)/gateware/$(litex_platform).bit
firmware_elf = $(soc_dir)/software/bios/bios.elf
firmware_bin = $(soc_dir)/software/bios/bios.bin


.DEFAULT_GOAL := all
.PHONY: all clean $(firmware_elf)

all: $(soc_dir)/qspi.bin build/$(litex_platform)/boot.scr $(soc_dir)/fpga.bin

$(firmware_elf):
	$(soc)

$(firmware_bin): $(firmware_elf)

$(bitstream_file):
	$(soc) --build --driver&& \
	grep -i "All user specified timing constraints are met" $(soc_dir)/gateware/vivado.log
	test -f $@

$(uboot_build_dir)/.config:
	make -C $(uboot_src_dir) O=${CURDIR}/$(uboot_build_dir) ARCH=arm DEVICE_TREE=$(uboot_device_tree) CROSS_COMPILE=arm-none-linux-gnueabihf- $(uboot_defconfig)

$(uboot_build_dir)/u-boot.img: $(uboot_build_dir)/.config
	make -C $(uboot_src_dir) O=${CURDIR}/$(uboot_build_dir) ARCH=arm DEVICE_TREE=$(uboot_device_tree) CROSS_COMPILE=arm-none-linux-gnueabihf- -j

$(uboot_build_dir)/spl/u-boot-spl.bin: $(uboot_build_dir)/u-boot.img

$(soc_dir)/boot_qspi.scr: scripts/boot_qspi.cmd
	$(uboot_build_dir)/tools/mkimage -C none -A arm -T script -d $< $@

$(soc_dir)/boot.scr: scripts/boot_sd.cmd
	$(uboot_build_dir)/tools/mkimage -C none -A arm -T script -d $< $@

ext_src/zynq-mkbootimage/mkbootimage:
	cd $(@D) && make

$(soc_dir)/qspi.bin: scripts/boot.bif $(bitstream_file) $(uboot_build_dir)/u-boot.img $(soc_dir)/boot_qspi.scr $(soc_dir)/software/bios/bios.bin $(uboot_build_dir)/spl/u-boot-spl.bin ext_src/zynq-mkbootimage/mkbootimage
	./ext_src/zynq-mkbootimage/mkbootimage $< $@

$(soc_dir)/fpga.bin: scripts/boot_fpga.bif $(bitstream_file) $(uboot_build_dir)/u-boot.img $(soc_dir)/boot_qspi.scr $(soc_dir)/software/bios/bios.bin $(uboot_build_dir)/spl/u-boot-spl.bin
	bootgen -image $< -arch zynq -process_bitstream bin -w -o $@

gateware: $(bitstream_file)

load: gateware
	$(soc) --load 
