#!/bin/bash

TLPPERF=$(cd $(dirname $0); pwd)/../libtlp/apps/tlpperf
OUTPUTDIR=$(cd $(dirname $0); pwd)/output-16b
NETTLP_NIC_ADDR=192.168.10.1

# parameters must be changed in accordance with TLP NIC host
# DMA_REGION_ADDR and size is decided by tlpperf -S
NETTLP_NIC_BUS=1b:00
DMA_REGION_ADDR=0x747400000
DMA_REGION_SIZE=8392704

# parameters for testing
DURATION=10

directions=(read)
dma_lens=(1 16 32 48 64 80 96 112 128 144 160 176 192 208 224 240 256 272 288 304 320 336 352 368 384 400 416 432 448 464 480 496 512 528 544 560 576 592 608 624 640 656 672 688 704 720 736 752 768 784 800 816 832 848 864 880 896 912 928 944 960 976 992 1008 1024 1040 1056 1072 1088 1104 1120 1136 1152 1168 1184 1200 1216 1232 1248 1264 1280 1296 1312 1328 1344 1360 1376 1392 1408 1424 1440 1456 1472 1488 1504 1520 1536 1552 1568 1584 1600 1616 1632 1648 1664 1680 1696 1712 1728 1744 1760 1776 1792 1808 1824 1840 1856 1872 1888 1904 1920 1936 1952 1968 1984 2000 2016 2032 2048)
cpu_nums=(16)
#patterns=(seq)
patterns=(fix)

iter=0
niter=$(( ${#directions[@]} * ${#patterns[@]} * ${#dma_lens[@]} * ${#cpu_nums[@]} ))

for direction in ${directions[@]}; do
for pattern in ${patterns[@]}; do
for dma_len in ${dma_lens[@]}; do
for cpu_num in ${cpu_nums[@]}; do

	iter=$(( $iter + 1 ))

	cmd=""
	cmd+="$TLPPERF -r $NETTLP_NIC_ADDR -b $NETTLP_NIC_BUS"
	cmd+=" -a $DMA_REGION_ADDR -s $DMA_REGION_SIZE"
	cmd+=" -d $direction -L $dma_len"
	cmd+=" -N $cpu_num -R diff -P $pattern"
	cmd+=" -t $DURATION"

	out=""
	out+="$OUTPUTDIR/${direction}_pattern-${pattern}_"
	out+="dmalen-${dma_len}_cpu-${cpu_num}.txt"

	echo Test No $iter / $niter
	echo Command: $cmd
	echo Output: $out
	echo
	$cmd > $out
done
done
done
done
