import sys
import hashlib
import math

class HyperLogLog:
    def __init__(self, b):
        self.b = b  # Number of bits for bucket index
        self.m = 1 << b  # Number of buckets (2^b)
        self.alphaMM = (0.7213 / (1 + 1.079 / self.m)) * self.m * self.m  # Constant for correction
        self.buckets = [0] * self.m

    def _hash(self, item):
        # Use hashlib to generate a hash
        return int(hashlib.md5(item.encode('utf8')).hexdigest(), 16)

    def add(self, item):
        x = self._hash(item)
        j = x >> (x.bit_length() - self.b)  # Get the bucket index
        w = x & ((1 << (x.bit_length() - self.b)) - 1)  # Remaining bits
        self.buckets[j] = max(self.buckets[j], self._rho(w))

    def _rho(self, w):
        # Count leading zeros
        return (w ^ (1 << w.bit_length() - 1)).bit_length() + 1

    def estimate(self):
        Z = 1.0 / sum(2 ** -mj for mj in self.buckets)
        E = self.alphaMM * Z  # Estimate using the bias correction

        # Apply bias correction for small cardinalities
        if E <= 2.5 * self.m:
            V = self.buckets.count(0)
            if V > 0:
                E = self.m * math.log(self.m / V)

        return E

if __name__ == "__main__":
    b = 14  # Choose the number of bits for the bucket index (log2 of number of buckets)
    hll = HyperLogLog(b)

    while True:
        line = sys.stdin.readline().strip()
        if not line:  # Break on empty input (if needed)
            break
        hll.add(line)
        print(f"Current estimate of unique items: {hll.estimate():.0f}")