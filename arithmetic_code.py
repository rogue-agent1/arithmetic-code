#!/usr/bin/env python3
"""Arithmetic coding compression."""
from collections import Counter

def build_ranges(freq: dict, total: int):
    ranges = {}
    low = 0
    for sym in sorted(freq.keys()):
        high = low + freq[sym]
        ranges[sym] = (low / total, high / total)
        low = high
    return ranges

def arithmetic_encode(data: bytes) -> tuple:
    if not data: return (0.0, {})
    freq = dict(Counter(data))
    total = len(data)
    ranges = build_ranges(freq, total)
    low = 0.0
    high = 1.0
    for byte in data:
        r = high - low
        sym_low, sym_high = ranges[byte]
        high = low + r * sym_high
        low = low + r * sym_low
    return ((low + high) / 2, freq)

def arithmetic_decode(value: float, freq: dict, length: int) -> bytes:
    if length == 0: return b""
    total = sum(freq.values())
    ranges = build_ranges(freq, total)
    inv = {}
    for sym, (lo, hi) in ranges.items():
        inv[sym] = (lo, hi)
    result = bytearray()
    for _ in range(length):
        for sym, (lo, hi) in inv.items():
            if lo <= value < hi:
                result.append(sym)
                value = (value - lo) / (hi - lo)
                break
    return bytes(result)

def test():
    data = b"AABBC"
    val, freq = arithmetic_encode(data)
    dec = arithmetic_decode(val, freq, len(data))
    assert dec == data, f"{dec} != {data}"
    # Single char
    data2 = b"AAAA"
    val2, freq2 = arithmetic_encode(data2)
    assert arithmetic_decode(val2, freq2, len(data2)) == data2
    # Empty
    val3, freq3 = arithmetic_encode(b"")
    assert arithmetic_decode(val3, freq3, 0) == b""
    print("  arithmetic_code: ALL TESTS PASSED")

if __name__ == "__main__":
    test()
