def fibonacci(n: int) -> int:
    """Calculates the nth Fibonacci number using an iterative approach."""
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    if n == 0:
        return 0
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
