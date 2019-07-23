
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
