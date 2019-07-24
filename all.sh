#!/bin/bash


for pattern in seq random fix; do
	./plot-x-cpu.py -d read -p $pattern -u bps
	./plot-x-cpu.py -d read -p $pattern -u tps -r M
	./plot-x-cpu.py -d write -p $pattern -u bps
	./plot-x-cpu.py -d write -p $pattern -u tps -r M
	./plot-x-dmalen.py -d read -p $pattern -u bps
	./plot-x-dmalen.py -d read -p $pattern -u tps -r M
	./plot-x-dmalen.py -d write -p $pattern -u bps
	./plot-x-dmalen.py -d write -p $pattern -u tps -r M
done

for pattern in seq seq512; do
	./plot-x-dmalen-16b-interval.py -p seq
	./plot-x-dmalen-16b-interval.py -p seq512
	./plot-x-dmalen-16b-interval.py -p fix
done
