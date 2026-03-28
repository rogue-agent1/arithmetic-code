#!/usr/bin/env python3
"""arithmetic_code - Arithmetic coding compression."""
import sys
from collections import Counter
from decimal import Decimal,getcontext
getcontext().prec=50
def build_ranges(freq):
    total=sum(freq.values());ranges={};low=Decimal(0)
    for char in sorted(freq):
        high=low+Decimal(freq[char])/Decimal(total);ranges[char]=(low,high);low=high
    return ranges
def encode(text):
    freq=Counter(text);ranges=build_ranges(freq)
    low,high=Decimal(0),Decimal(1)
    for c in text:
        rng=high-low;low=low+rng*ranges[c][0];high=low+rng*(ranges[c][1]-ranges[c][0])
    return(low+high)/2,freq,len(text)
def decode(value,freq,length):
    ranges=build_ranges(freq);result=[]
    for _ in range(length):
        for char,(lo,hi) in ranges.items():
            if lo<=value<hi:
                result.append(char);rng=hi-lo;value=(value-lo)/rng;break
    return"".join(result)
if __name__=="__main__":
    text=sys.argv[1] if len(sys.argv)>1 else "abracadabra"
    val,freq,length=encode(text)
    print(f"Encoded: {val}");decoded=decode(val,freq,length)
    print(f"Decoded: {decoded}");print(f"Match: {text==decoded}")
