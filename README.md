In Python, and other languages, a standard double-precision float can represent values roughly between 1e308 and 1e-308.

In order to bypass this, we must separate the mantissa (a) from the exponent (b) in the equation n = a * 10^b,
where 1 <= a < 10, and b is a whole number.

As such, if either a < 1 or a > 10 is true, the values should be normalized.
If a = 0, we can skip everything as x * 0 = 0.

If 'b', the exponent, has a fractional part (f), we should also multiply 'a', the mantissa by 10^f.

All of this allows us to represent numbers up to roughly 10^10^308, 1e1e308, or 1ee308,
as the exponent itself has now become the limiting factor.