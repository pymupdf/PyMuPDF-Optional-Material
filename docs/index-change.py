import sys
import os

fn = sys.argv[1]

lines = open(fn).read().splitlines()
outlines = []
for line in lines:
    if "pair: " not in line or line.endswith(")"):
        outlines.append(line)
        continue
    items = line.split(";")
    refs = items[-1].split(".")
    the_class = refs[0].strip()
    new_ref = refs[1] + " (" + the_class + ")"
    line = items[0] + "; " + new_ref
    outlines.append(line)

outfile = open("new-" + fn, "w")
outfile.write("\n".join(outlines))
outfile.close()
