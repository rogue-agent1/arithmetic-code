#!/usr/bin/env python3
"""arithmetic_code - Arithmetic coding implementation."""
import sys, collections
def get_probs(text):
    freq=collections.Counter(text); n=len(text)
    probs={}; cumulative=0.0
    for char in sorted(freq):
        p=freq[char]/n; probs[char]=(cumulative, cumulative+p); cumulative+=p
    return probs
def encode(text):
    probs=get_probs(text); low=0.0; high=1.0
    for char in text:
        r=high-low; high=low+r*probs[char][1]; low=low+r*probs[char][0]
    return (low+high)/2, probs
def decode(value, length, probs):
    result=[]; inv={v:k for k,v in probs.items()}
    for _ in range(length):
        for char,(lo,hi) in probs.items():
            if lo<=value<hi:
                result.append(char); value=(value-lo)/(hi-lo); break
    return "".join(result)
if __name__=="__main__":
    text=sys.argv[1] if len(sys.argv)>1 else "ABRACADABRA"
    value,probs=encode(text)
    decoded=decode(value, len(text), probs)
    print(f"Original: {text}"); print(f"Encoded value: {value:.15f}")
    print(f"Decoded: {decoded} (match: {decoded==text})")
    print(f"Probabilities: {probs}")
