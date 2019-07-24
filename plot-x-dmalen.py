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
    parser.add_argument("-d", "--direction", help = "DMA direction",
                        choices = ["read", "write"], default = "read")
    parser.add_argument("-c", "--cpunum", help = "CPU nums to be drawn",
                        action = "append", type = int)
    parser.add_argument("-l", "--dmalen", help = "DMA len to be drawn",
                        action = "append", type = int)
    parser.add_argument("-x", "--xticks", help = "xticks value",
                        action = "append", type = int)
    parser.add_argument("-p", "--pattern", help = "access pattern",
                        choices = ["seq", "fix", "random"], default = "seq")
    parser.add_argument("-r", "--round", help = "round up x axis",
                        choices = round_map.keys(),
                        default = list(round_map.keys())[0])
    parser.add_argument("-R", "--ratio", help = "aspect ratio",
                        type = float, default = ratio)
    parser.add_argument("-o", "--output", help = "output pdf file name",
                        default = None)
    args = parser.parse_args()

    if not args.cpunum:
        cpu_nums = [ 1, 2, 4, 6, 8, 10, 12, 14, 16]
    else:
        cpu_nums = args.cpunum

    if not args.dmalen:
        dma_lens = [ 1, 4, 8, 16, 32, 64, 128, 256, 512, 1024 ]
    else:
        dma_lens = args.dmalen

    if not args.xticks:
        xticks = [1, 128, 256, 512, 1024]
    else:
        xticks = args.xticks

    if not args.output:
        pdffile = ("graph/graph_{}_x-dmalen_".format(args.direction) +
                   "pattern-{}_".format(args.pattern) +
                   "{}.pdf".format(args.unit))
    else:
        pdffile = args.output


    fig, ax= plt.subplots()

    maximum = 0

    for cpu_num in cpu_nums:

        bpses = []
        tpses = []

        for dma_len in dma_lens:

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

        ax.plot(dma_lens, yaxis, marker = get_marker(), color = get_color(),
                label = "{} cores".format(cpu_num))

        # save maxsimum y value
        if maximum < max(yaxis):
            maximum = max(yaxis)

    yticks = list(range(int(maximum) + 2)) # this code depends on round up Gig
    plt.yticks(yticks, yticks)
    #plt.xticks(dma_lens, dma_lens)
    plt.xticks(xticks)

    ax.tick_params(labelsize = fontsize)
    ax.set_ylabel("throughput ({}{})".format(args.round, args.unit),
                  fontsize = fontsize)
    ax.set_xlabel("transferr size (byte)", fontsize = fontsize)

    ax.grid(True, linestyle = "--", linewidth = 0.5)
    ax.legend(fontsize = lfontsize)

    change_aspect_ratio(ax, args.ratio)
    
    print("save '{}'".format(pdffile))
    plt.savefig(pdffile, bbox_inches = "tight", pad_inches = 0.05)


if __name__ == "__main__":
    main()
