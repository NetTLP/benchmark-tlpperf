#!/usr/bin/env python

import argparse
import matplotlib.pyplot as plt
import matplotlib
from myplotlib import get_marker, get_color, get_linestyle, change_aspect_ratio

from tlpperfparser import parse, parse_lat

fontsize = 22
lfontsize = 18
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

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--direction", help = "DMA direction",
                        choices = ["read", "write"], default = "read")
    parser.add_argument("-l", "--dmalen", help = "DMA length to be drawn",
                        action = "append")
    parser.add_argument("-p", "--pattern", help = "access pattern",
                        choices = ["seq", "fix", "random"], default = "seq")
    parser.add_argument("-R", "--ratio", help = "aspect ratio",
                        type = float, default = 1.5)
    parser.add_argument("-o", "--output", help = "output pdf file name",
                        default = None)
    args = parser.parse_args()

    if not args.dmalen:
        dma_lens = [ 1, 4, 8, 16, 32, 64, 128, 256, 512, 1024 ]
    else:
        dma_lens = args.dmalen
    cpu_nums = [ 1 ]

    if not args.output:
        pdffile = ("graph/graph_latency_{}_".format(args.direction) +
                   "pattern-{}.pdf".format(args.pattern))

    else:
        pdffile = args.output

    fig, ax= plt.subplots()

    maximum = 0

    for dma_len in dma_lens:

        for cpu_num in cpu_nums:
            f = ("output-lat/{}_".format(args.direction) +
                 "pattern-{}_".format(args.pattern) + 
                 "dmalen-{}_".format(dma_len) +
                 "cpu-{}.txt".format(cpu_num))

        xaxis, yaxis = parse_lat(f)

        ax.plot(xaxis, yaxis, color = get_color(), linestyle = get_linestyle(),
                label = "DMA {}B".format(dma_len))

        # save maximum x value
        if maximum < max(xaxis) :
            maximum = max(xaxis)

    #xticks = list(range(int(maximum) + 2))
    #plt.xticks(xticks, xticks)
    plt.yticks(list(map(lambda x: x * 0.2, range(0, 6))))

    ax.tick_params(labelsize = fontsize)
    ax.set_ylabel("CDF", fontsize = fontsize)
    ax.set_xlabel("latency (usec)", fontsize = fontsize)

    ax.grid(True, linestyle = "--", linewidth = 0.5)
    ax.legend(fontsize = lfontsize, loc = "lower right")

    change_aspect_ratio(ax, args.ratio)
    
    print("save '{}'".format(pdffile))
    plt.savefig(pdffile, bbox_inches = "tight", pad_inches = 0.05)


if __name__ == "__main__":
    main()
