
import re
import statistics as st

def parse(filename):

    bps = []
    tps = []

    with open(filename, "r") as f:
        for line in f:
            l = line.strip()
            if re.match(r'^\d+:', l):
                n, v, r = l.split(" ")
                if r == "bps":
                    bps.append(int(v))
                elif r == "tps":
                    tps.append(int(v))

    return st.mean(bps), st.mean(tps)


def parse_lat(filename):

    lats = []

    with open(filename, "r") as f:
        for line in f:
            l = line.strip()
            if re.match(r'^latency:', l):
                s = l.split(' ')
                lats.append(int(s[4]))

    return cdf(lats)

def cdf(lats, bin = 1):
    
    # bin is usec

    xaxis = []
    yaxis = []
    values = sorted(lats)

    cnt = 0
    start = 0
    num_of_values = 0
    
    while True:
        
        thresh = cnt * bin

        for x in range(start, len(values)):
            v = values[x]
            if v <= thresh:
                num_of_values += 1
            else:
                start = x
                break
        
        ratio = num_of_values / len(values)
        xaxis.append(thresh)
        yaxis.append(ratio)
        cnt += 1

        if num_of_values == len(values):
            break

    return xaxis, yaxis
