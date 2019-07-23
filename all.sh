#!/bin/bash


for pattern in seq random fix; do
	./plot-x-cpu.py -d read -p $pattern -u bps
	./plot-x-cpu.py -d read -p $pattern -u tps
	./plot-x-cpu.py -d write -p $pattern -u bps
	./plot-x-cpu.py -d write -p $pattern -u tps
done
	
	
