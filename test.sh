#!/bin/bash

TLPPERF=$(cd $(dirname $0); pwd)/../libtlp/apps/tlpperf
OUTPUTDIR=$(cd $(dirname $0); pwd)/output
NETTLP_NIC_ADDR=192.168.10.1

# parameters must be changed in accordance with TLP NIC host
# DMA_REGION_ADDR and size is decided by tlpperf -S
NETTLP_NIC_BUS=1b:00
DMA_REGION_ADDR=0x747400000
DMA_REGION_SIZE=8392704

# parameters for testing
DURATION=10

directions=(read write)
#dma_lens=(1 4 8 16 32 64 128 256)
dma_lens=(512)
cpu_nums=(1 2 4 6 8 10 12 14 16)
patterns=(fix seq random)

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
