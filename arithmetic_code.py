#!/usr/bin/env python3
"""arithmetic_code - Arithmetic coding for compression."""
import sys
from collections import Counter

def build_model(data):
    freq = Counter(data)
    total = len(data)
    cumulative = {}
    low = 0
    for symbol in sorted(freq.keys()):
        high = low + freq[symbol]
        cumulative[symbol] = (low / total, high / total)
        low = high
    return cumulative

def arithmetic_encode(data, model):
    low, high = 0.0, 1.0
    for symbol in data:
        rng = high - low
        sym_low, sym_high = model[symbol]
        high = low + rng * sym_high
        low = low + rng * sym_low
    return (low + high) / 2

def arithmetic_decode(value, model, length):
    result = []
    for _ in range(length):
        for symbol, (sym_low, sym_high) in sorted(model.items()):
            if sym_low <= value < sym_high:
                result.append(symbol)
                rng = sym_high - sym_low
                value = (value - sym_low) / rng
                break
    return result

def test():
    data = "ABRACADABRA"
    model = build_model(data)
    assert len(model) == 5
    for sym in model:
        lo, hi = model[sym]
        assert 0 <= lo < hi <= 1
    encoded = arithmetic_encode(data, model)
    assert 0 < encoded < 1
    decoded = arithmetic_decode(encoded, model, len(data))
    assert "".join(decoded) == data
    data2 = "AAABBB"
    m2 = build_model(data2)
    e2 = arithmetic_encode(data2, m2)
    d2 = arithmetic_decode(e2, m2, len(data2))
    assert "".join(d2) == data2
    data3 = "X"
    m3 = build_model(data3)
    e3 = arithmetic_encode(data3, m3)
    d3 = arithmetic_decode(e3, m3, 1)
    assert d3 == ["X"]
    print("All tests passed!")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("arithmetic_code: Arithmetic coding. Use --test")
