#!/usr/bin/env python3
"""arithmetic_code - Arithmetic coding with adaptive models."""
import sys, argparse, json, collections

PRECISION = 32
WHOLE = 1 << PRECISION
HALF = WHOLE >> 1
QUARTER = WHOLE >> 2

def arithmetic_encode(data, freq=None):
    if not data: return [], {}
    if freq is None: freq = collections.Counter(data)
    total = sum(freq.values())
    cum = {}; running = 0
    for sym in sorted(freq.keys()):
        cum[sym] = (running, running + freq[sym])
        running += freq[sym]
    lo, hi = 0, WHOLE; pending = 0; bits = []
    def emit(bit):
        nonlocal pending
        bits.append(bit)
        while pending > 0: bits.append(1 - bit); pending -= 1
    for sym in data:
        rng = hi - lo
        sym_lo, sym_hi = cum[sym]
        hi = lo + rng * sym_hi // total
        lo = lo + rng * sym_lo // total
        while True:
            if hi <= HALF: emit(0)
            elif lo >= HALF: emit(1); lo -= HALF; hi -= HALF
            elif lo >= QUARTER and hi <= 3 * QUARTER:
                pending += 1; lo -= QUARTER; hi -= QUARTER
            else: break
            lo <<= 1; hi <<= 1
    pending += 1
    emit(1 if lo >= QUARTER else 0)
    return bits, freq

def arithmetic_decode(bits, freq, length):
    total = sum(freq.values())
    cum = {}; running = 0
    for sym in sorted(freq.keys()):
        cum[sym] = (running, running + freq[sym])
        running += freq[sym]
    lo, hi = 0, WHOLE; value = 0; bit_idx = 0
    for i in range(PRECISION):
        value = (value << 1) | (bits[bit_idx] if bit_idx < len(bits) else 0)
        bit_idx += 1
    result = []
    for _ in range(length):
        rng = hi - lo
        scaled = ((value - lo + 1) * total - 1) // rng
        for sym in sorted(freq.keys()):
            sym_lo, sym_hi = cum[sym]
            if sym_lo <= scaled < sym_hi:
                result.append(sym)
                hi = lo + rng * sym_hi // total
                lo = lo + rng * sym_lo // total
                break
        while True:
            if hi <= HALF: pass
            elif lo >= HALF: lo -= HALF; hi -= HALF; value -= HALF
            elif lo >= QUARTER and hi <= 3*QUARTER:
                lo -= QUARTER; hi -= QUARTER; value -= QUARTER
            else: break
            lo <<= 1; hi <<= 1
            value = (value << 1) | (bits[bit_idx] if bit_idx < len(bits) else 0)
            bit_idx += 1
    return "".join(result)

def main():
    p = argparse.ArgumentParser(description="Arithmetic coding")
    p.add_argument("--demo", action="store_true")
    args = p.parse_args()
    if args.demo:
        texts = ["ABRACADABRA", "hello world hello world", "aaaaaabbbbccd",
                 "the quick brown fox jumps over the lazy dog"]
        for text in texts:
            bits, freq = arithmetic_encode(text)
            decoded = arithmetic_decode(bits, freq, len(text))
            ok = decoded == text
            ratio = len(bits) / (len(text) * 8)
            entropy = -sum(f/sum(freq.values()) * (f/sum(freq.values())).bit_length() for f in freq.values() if f > 0) if False else 0
            print(f"[{'OK' if ok else 'FAIL'}] \"{text[:30]}\" {len(bits)} bits ({ratio:.1%})")
    else: p.print_help()
if __name__ == "__main__": main()
