"""Example module with intentional bugs for clauder heal demo."""


def add(a, b):
    return a + b


def subtract(a, b):
    # Bug: wrong operator
    return a + b


def multiply(a, b):
    # Bug: only uses first argument
    return a * a


def divide(a, b):
    # Bug: no zero-division guard
    return a / b


def factorial(n):
    # Bug: missing base case
    return n * factorial(n - 1)
