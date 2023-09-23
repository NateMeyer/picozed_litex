dcache off

fatload mmc 0 0x100000 picozed_z7030.bit
fpga loadb 0 0x100000 ${filesize}

fatload mmc 0 0x100000 bios.bin
go 0x100000