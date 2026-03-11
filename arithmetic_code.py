#!/usr/bin/env python3
"""Arithmetic coding — near-optimal entropy compression."""
import sys
from collections import Counter

def get_ranges(text):
    freq = Counter(text); total = len(text)
    ranges = {}; lo = 0.0
    for c in sorted(freq):
        hi = lo + freq[c] / total
        ranges[c] = (lo, hi); lo = hi
    return ranges

def encode(text):
    ranges = get_ranges(text)
    lo, hi = 0.0, 1.0
    for c in text:
        r = hi - lo
        clo, chi = ranges[c]
        hi = lo + r * chi
        lo = lo + r * clo
    return (lo + hi) / 2, ranges

def decode(value, length, ranges):
    inv = {v: k for k, v in ranges.items()}
    result = []
    for _ in range(length):
        for c, (clo, chi) in ranges.items():
            if clo <= value < chi:
                result.append(c)
                value = (value - clo) / (chi - clo)
                break
    return "".join(result)

if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) or "abracadabra"
    value, ranges = encode(text)
    decoded = decode(value, len(text), ranges)
    entropy = -sum(f/len(text) * __import__('math').log2(f/len(text)) for f in Counter(text).values())
    print(f"Text:    {text!r}")
    print(f"Value:   {value:.15f}")
    print(f"Decoded: {decoded!r}")
    print(f"Correct: {decoded == text}")
    print(f"Entropy: {entropy:.3f} bits/symbol")
    print(f"Theoretical minimum: {entropy * len(text):.1f} bits")
