#!/usr/bin/env python

import argparse
import matplotlib.pyplot as plt
import matplotlib
from myplotlib import get_marker, get_color, change_aspect_ratio

from tlpperfparser import parse

fontsize = 14
lfontsize = 12
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
    parser.add_argument("-d", "--direction", help = "DMA direction",
                        choices = ["read", "write"], default = "read")
    parser.add_argument("-l", "--dmalen", help = "DMA length to be drawn",
                        action = "append")
    parser.add_argument("-p", "--pattern", help = "access pattern",
                        choices = ["seq", "fix", "random"], default = "seq")
    parser.add_argument("-r", "--round", help = "round up x axis",
                        choices = round_map.keys(),
                        default = list(round_map.keys())[0])
    parser.add_argument("-R", "--ratio", help = "aspect ratio",
                        type = float, default = 1.5)
    parser.add_argument("-o", "--output", help = "output pdf file name",
                        default = None)
    args = parser.parse_args()

    if not args.dmalen:
        dma_lens = reversed([ 1, 4, 8, 16, 32, 64, 128, 256, 512, 1024 ])
    else:
        dma_lens = args.dmalen
    cpu_nums = [ 1, 2, 4, 6, 8, 10, 12, 14, 16]

    if not args.output:
        pdffile = ("graph/graph_{}_x-cpu_".format(args.direction) +
                   "pattern-{}_".format(args.pattern) +
                   "{}.pdf".format(args.unit))
    else:
        pdffile = args.output

    fig, ax= plt.subplots()

    maximum = 0

    for dma_len in dma_lens:

        bpses = []
        tpses = []

        for cpu_num in cpu_nums:
            f = ("output/{}_".format(args.direction) +
                 "pattern-{}_".format(args.pattern) + 
                 "dmalen-{}_".format(dma_len) +
                 "cpu-{}.txt".format(cpu_num))

            bps, tps = parse(f)
            bpses.append(bps)
            tpses.append(tps)

        if args.unit == "bps":
            yaxis = bpses
        elif args.unit == "tps":
            yaxis = tpses

        # round up to K, M, or G
        yaxis = list(map(lambda x: x / round_map[args.round], yaxis))

        ax.plot(cpu_nums, yaxis, marker = get_marker(), color = get_color(),
                label = "DMA {}B".format(dma_len))

        # save maximum y value
        if maximum < max(yaxis) :
            maximum = max(yaxis)

    yticks = list(range(int(maximum) + 2)) # this code depends on round up Gig
    plt.yticks(yticks, yticks)
    plt.xticks(cpu_nums, cpu_nums)

    ax.tick_params(labelsize = fontsize)
    ax.set_ylabel("throughput ({}{})".format(args.round, args.unit),
                  fontsize = fontsize)
    ax.set_xlabel("number of cores", fontsize = fontsize)

    ax.grid(True, linestyle = "--", linewidth = 0.5)
    ax.legend(fontsize = lfontsize)

    change_aspect_ratio(ax, args.ratio)
    
    print("save '{}'".format(pdffile))
    plt.savefig(pdffile, bbox_inches = "tight", pad_inches = 0.05)


if __name__ == "__main__":
    main()
