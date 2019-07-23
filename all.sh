#!/bin/bash


for pattern in seq random fix; do
	./plot-x-cpu.py -p $pattern -u bps
	./plot-x-cpu.py -p $pattern -u tps
done
	
