"""Mathematical sequences used as source material for composition."""

from typing import Iterator, List
import math


def fibonacci(n: int) -> List[int]:
    """Returns the first n Fibonacci numbers."""
    seq = [1, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq[:n]


def primes(n: int) -> List[int]:
    """Returns the first n prime numbers using the Sieve of Eratosthenes."""
    sieve_limit = max(15, n * 15)
    sieve = [True] * (sieve_limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(math.sqrt(sieve_limit)) + 1):
        if sieve[i]:
            for j in range(i * i, sieve_limit + 1, i):
                sieve[j] = False
    result = [i for i, is_prime in enumerate(sieve) if is_prime]
    return result[:n]


def collatz(start: int) -> List[int]:
    """Returns the Collatz sequence starting from `start` until it reaches 1."""
    seq = [start]
    n = start
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        seq.append(n)
    return seq


def golden_ratio(n: int) -> List[float]:
    """Returns n terms of the golden ratio convergents as integers (×1000)."""
    phi = (1 + math.sqrt(5)) / 2
    return [int((phi ** i) % 100 * 10) for i in range(1, n + 1)]


def mandelbrot_sequence(
    real_range: tuple = (-2.0, 0.5),
    imag_range: tuple = (-1.25, 1.25),
    steps: int = 32,
    max_iter: int = 64,
) -> List[int]:
    """
    Samples the Mandelbrot set along a diagonal path and returns
    iteration counts — higher values = points near the boundary (chaos).
    """
    result = []
    for i in range(steps):
        t = i / (steps - 1)
        real = real_range[0] + t * (real_range[1] - real_range[0])
        imag = imag_range[0] + t * (imag_range[1] - imag_range[0])
        c = complex(real, imag)
        z = 0
        count = 0
        while abs(z) <= 2 and count < max_iter:
            z = z * z + c
            count += 1
        result.append(count)
    return result


def triangular(n: int) -> List[int]:
    """Returns the first n triangular numbers: 1, 3, 6, 10, 15, ..."""
    return [i * (i + 1) // 2 for i in range(1, n + 1)]


def look_and_say(n: int) -> List[int]:
    """
    Generates the Look-and-Say sequence and returns the digit lengths
    of the first n terms — famously grows at Conway's constant ~1.303.
    """
    s = "1"
    lengths = [1]
    for _ in range(n - 1):
        new_s = ""
        i = 0
        while i < len(s):
            digit = s[i]
            count = 1
            while i + count < len(s) and s[i + count] == digit:
                count += 1
            new_s += str(count) + digit
            i += count
        s = new_s
        lengths.append(len(s))
    return lengths
