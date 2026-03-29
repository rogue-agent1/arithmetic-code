#!/usr/bin/env python3
"""arithmetic_code - Arithmetic coding with adaptive model."""
import argparse
from collections import defaultdict

class ArithmeticEncoder:
    def __init__(self, precision=32):
        self.precision=precision;self.full=1<<precision
        self.half=self.full>>1;self.quarter=self.half>>1
        self.lo=0;self.hi=self.full-1;self.pending=0;self.bits=[]
    def encode_symbol(self, cum_freq, sym_lo, sym_hi, total):
        rng=self.hi-self.lo+1
        self.hi=self.lo+rng*sym_hi//total-1
        self.lo=self.lo+rng*sym_lo//total
        while True:
            if self.hi<self.half:
                self._output(0)
            elif self.lo>=self.half:
                self._output(1);self.lo-=self.half;self.hi-=self.half
            elif self.lo>=self.quarter and self.hi<3*self.quarter:
                self.pending+=1;self.lo-=self.quarter;self.hi-=self.quarter
            else: break
            self.lo<<=1;self.hi=(self.hi<<1)|1
    def _output(self, bit):
        self.bits.append(bit)
        while self.pending: self.bits.append(1-bit);self.pending-=1
    def finish(self):
        self.pending+=1
        self._output(0 if self.lo<self.quarter else 1)
        return self.bits

class AdaptiveModel:
    def __init__(self, alphabet_size=256):
        self.size=alphabet_size+1;self.freq=[1]*self.size
        self.total=self.size
    def get_range(self, symbol):
        lo=sum(self.freq[:symbol]);hi=lo+self.freq[symbol]
        return lo,hi,self.total
    def update(self, symbol):
        self.freq[symbol]+=1;self.total+=1

def compress(text):
    model=AdaptiveModel();enc=ArithmeticEncoder()
    for c in text:
        s=ord(c);lo,hi,total=model.get_range(s)
        enc.encode_symbol(None,lo,hi,total);model.update(s)
    lo,hi,total=model.get_range(256)
    enc.encode_symbol(None,lo,hi,total)
    return enc.finish()

def main():
    p=argparse.ArgumentParser(description="Arithmetic coding")
    p.add_argument("--text",default="abracadabra")
    args=p.parse_args()
    bits=compress(args.text)
    orig=len(args.text)*8
    comp=len(bits)
    entropy=0
    freq=defaultdict(int)
    for c in args.text: freq[c]+=1
    import math
    for c,f in freq.items():
        p=f/len(args.text)
        entropy-=p*math.log2(p)
    theoretical=int(entropy*len(args.text))
    print(f"Text: '{args.text}' ({len(args.text)} chars)")
    print(f"Original: {orig} bits")
    print(f"Compressed: {comp} bits ({comp/orig*100:.1f}%)")
    print(f"Theoretical minimum: {theoretical} bits (entropy={entropy:.2f} bits/sym)")
    print(f"Efficiency: {theoretical/comp*100:.1f}%")

if __name__=="__main__":
    main()
