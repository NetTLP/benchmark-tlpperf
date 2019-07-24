#!/bin/bash

./plot-x-cpu.py -d read -l 256 -l 512 -l 1024 -r G -R 2 \
	-o graph/graph-paper_x-cpuw_read.pdf

./plot-x-cpu.py -d write -l 128 -l 256 -l 512 -r G -R 2 \
	-o graph/graph-paper_x-cpu_write.pdf


./plot-x-dmalen.py -d read -c 1 -c 16 -r G -R 2 \
	-o graph/graph-paper_x-dmalen_read.pdf

./plot-x-dmalen.py -d write -c 1 -c 16 -r G -R 2 \
	-l 1 -l 4 -l 8 -l 16 -l 32 -l 64 -l 128 -l 256 -l 512 \
	-x 1 -x 32 -x 64 -x 128 -x 256 -x 512 \
	-o graph/graph-paper_x-dmalen_write.pdf


./plot-x-dmalen-16b-interval.py -p seq -R 2 \
	-o graph/graph-paper_x-dmalen-16binterval_pattern_seq.pdf

./plot-x-dmalen-16b-interval.py -p fix -R 2 \
	-o graph/graph-paper_x-dmalen-16binterval_pattern_fix.pdf


./plot-lat.py -l 1 -l 256 -l 1024 -p fix -R 3 \
	-o graph/graph-paper_latency_read_fix.pdf
