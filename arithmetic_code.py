#!/usr/bin/env python3
"""arithmetic_code: Arithmetic coding compression."""
import sys

def build_model(data):
    freq = {}
    for c in data: freq[c] = freq.get(c, 0) + 1
    total = len(data)
    cumulative = {}
    low = 0
    for c in sorted(freq):
        cumulative[c] = (low, low + freq[c])
        low += freq[c]
    return cumulative, total

def encode(data):
    model, total = build_model(data)
    lo, hi = 0, 1 << 32
    for c in data:
        rng = hi - lo
        clo, chi = model[c]
        hi = lo + (rng * chi) // total
        lo = lo + (rng * clo) // total
    return (lo + hi) // 2, len(data), model, total

def decode(code, length, model, total):
    reverse = {}
    for c, (clo, chi) in model.items():
        for i in range(clo, chi):
            reverse[i] = c
    lo, hi = 0, 1 << 32
    result = []
    for _ in range(length):
        rng = hi - lo
        scaled = ((code - lo) * total) // rng
        scaled = min(scaled, total - 1)
        c = reverse[scaled]
        result.append(c)
        clo, chi = model[c]
        hi = lo + (rng * chi) // total
        lo = lo + (rng * clo) // total
    return "".join(result)

def test():
    text = "abracadabra"
    code, length, model, total = encode(text)
    decoded = decode(code, length, model, total)
    assert decoded == text
    # Repeated
    text2 = "aaaaaaa"
    c2, l2, m2, t2 = encode(text2)
    assert decode(c2, l2, m2, t2) == text2
    # Two chars
    text3 = "ababab"
    c3, l3, m3, t3 = encode(text3)
    assert decode(c3, l3, m3, t3) == text3
    # Single char
    text4 = "x"
    c4, l4, m4, t4 = encode(text4)
    assert decode(c4, l4, m4, t4) == text4
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: arithmetic_code.py test")
