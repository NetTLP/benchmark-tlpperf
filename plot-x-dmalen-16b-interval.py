#!/usr/bin/env python

import argparse
import matplotlib.pyplot as plt
import matplotlib
from myplotlib import get_marker, get_color, change_aspect_ratio

from tlpperfparser import parse

ratio = 1.5
fontsize = 14
lfontsize = 13.5
markersize = 11
linewidth = 2.4
lines = { "linewidth" : linewidth,
          "markersize" : markersize,
          "markeredgewidth" : linewidth, }
markers = { "fillstyle" : "none", }
plt.rc("lines", **lines)
plt.rc("markers", **markers)
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42


def main():

    round_map = {
        "G": 1000000000,
        "M": 1000000,
        "K": 1000,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--unit", help = "unit of bandwidth",
                        choices = ["bps", "tps"], default = "bps")
    parser.add_argument("-p", "--pattern", help = "access pattern",
                        choices = ["seq", "fix", "random"], default = "seq")
    parser.add_argument("-r", "--round", help = "round up x axis",
                        choices = round_map.keys(),
                        default = list(round_map.keys())[0])
    args = parser.parse_args()

    dma_lens = list(map(lambda x: x * 16, range(129)))
    dma_lens[0] = 1
    xaxis = list(map(lambda x: x * 256, range(9)))

    pdffile = ("graph/graphx_dmalen-16binterval" +
               "pattern-{}_{}.pdf".format(args.pattern, args.unit))
               


    fig, ax= plt.subplots()

    bpses = []
    tpses = []

    for dma_len in dma_lens:
        f = ("output-16b/read_pattern-{}_".format(args.pattern) +
             "dmalen-{}_".format(dma_len) +
             "cpu-16.txt")
         
        bps, tps = parse(f)
        bpses.append(bps)
        tpses.append(tps)

    if args.unit == "bps":
        yaxis = bpses
    elif args.unit == "tps":
        yaxis = tpses

    # round up to K, M, or G
    yaxis = list(map(lambda x: x / round_map[args.round], yaxis))

    ax.plot(dma_lens, yaxis, color = get_color())

    plt.xticks(xaxis)
    ax.tick_params(labelsize = fontsize)
    ax.set_ylabel("throughput ({}{})".format(args.round, args.unit),
                  fontsize = fontsize)
    ax.set_xlabel("transfer size (byte)", fontsize = fontsize)

    ax.grid(True, linestyle = "--", linewidth = 0.5)

    change_aspect_ratio(ax, ratio)
    
    plt.savefig(pdffile, bbox_inches = "tight", pad_inches = 0.05)


if __name__ == "__main__":
    main()
