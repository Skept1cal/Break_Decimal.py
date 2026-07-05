A numerical library for Python, largely inspired by https://github.com/Patashu/break_infinity.js.

This library *should* be able to work with and represent values up to around ~1ee308 (10<sup>10<sup>308</sup></sup>), as opposed to standard floats which cap out at ~1.797e308,
or 1.797 * 10<sup>308</sup>.

The library supports most if not all basic operations, floor division, general logarithms, and has a built-in display function with different formats.

Please don't expect this to be perfect, I'm not particularly great at coding, and this was more of a passion project than something to be perfect, or near-perfect.
Thank you.

### Note:

Despite the name, this library is not made with high precision in mind. If you want precision, please use Python's built in Decimal module/package.

## Importing

In order to use the package, you must install it on your computer with:

```python
pip install git+https://github.com/Skept1cal/Break_Decimal.py
```

Then, you can import it into any project through:

```python
from Break_Decimal import Decimal
```

or:

```python
import Break_Decimal as breakdec
```

## Functions

### Unique stand-alones:

```python
x = Decimal("1e456") # Creates a Decimal class object with a tuple as attribute 'value'

# Normalizes input value 'x' into a tuple, representing the standard form 'a * 10^b'. norm(x) can be used as an alias if desired.
normalize(x) 
norm(x)

bigmax(n1, n2) # Returns the greater value out of 'n1' and 'n2'
bigmin(n1, n2) # Returns the smaller value out of 'n1' and 'n2'
```

### Methods:

```python

# Absolute value ----------:

self._abs() # Base function
abs(self) # Allows usage of the regular abs() function in Python

_abs(n) # Its stand-alone version

# Greater than (x > y) ----------:

self.gt(other) # Base function
self > other # With symbols

gt(n1, n2) # Its stand-alone version

# Greater than or equal to (x >= y) ----------:

self.gte(other) # Base function
self >= other # With symbols

gte(n1, n2) # Its stand-alone version

# Less than (x < y) ----------:

self.lt(other) # Base function
self < other # With symbols

lt(n1, n2) # Its stand-alone version

# Less than or equal to (x <= y) ----------:

self.lte(other) # Base function
self <= other # With symbols

lte(n1, n2) # Its stand-alone version

# Equal to (x == y) ----------:

self.eq(other) # Base function
self == other # With symbols

eq(n1, n2) # Its stand-alone version

# Not equal to (x != y) ----------:

self.neq(other) # Base function
self != other # With symbols

neq(n1, n2) # Its stand-alone version

```

***NOTE: LOGARITHMS DO NOT TAKE NEGATIVE VALUES.***

```python

# Logarithms ----------:

self.log(base) # Base-'base' logarithm
log(n, base) # Its stand-alone version

self.log10() # Base-10 logarithm
log10(n) # Its stand-alone version

self.log2() # Base-2 logarithm
log2(n) # Its stand-alone version

self.ln() # Natural logarithm (base-~2.71828)
ln(n) # Its stand-alone version

# Exponentiation (base ** exp) ----------:

self.pow(n) # Base function
self ** n # With symbols

pow(base, exp) # Its stand-alone version

# Roots ----------:

self.root(n) # Base function: 'n'th root of 'self'

# Alternatively, you can use 'pow' to calculate roots, by inputting 'n ** -1'. Be careful, though; you can only do this if 'n' is 'Decimal', 'int', or 'float'.
self.pow(pow(n, -1))

root(base, root) # Its stand-alone version

# Multiplication (a * b) ----------:

self.mult(n) # Base function
self.mul(n) # Slightly shorter alias
self * n # With symbols

mult(a, b) # Its stand-alone version
mul(a, b) # Slightly shorter alias

# Division (a / b) ----------:

self.div(n) # Base function
self / n # With symbols

div(a, b) # Its stand-alone version

# Floor division (a // b); performs the operation on the mantissa by default ----------:

self.fdiv(n) # Base function
self // n # With symbols

fdiv(a, b) # Its stand-alone version

# If needed, 'self.truefdiv(n)' or truefdiv(a, b) can be used to perform floor division on the full number:

self.truefdiv(n) # Base function
truefdiv(a, b) # Its stand-alone version

# Addition (x + y) ----------:

self.add(n) # Base function
self + n # With symbols

add(n1, n2) # Its stand-alone version

# Subtraction (x - y) ----------:

self.sub(n) # Base function
self - n # With symbols

sub(n1, n2) # Its stand-alone version

```

### How to use the `disp()` function

You can display a Decimal more elegantly using:

```python
self.disp(s, form)
```

or:

```python
disp(n, s, form)
```

In order to display a Decimal (or a number of virtually any other type), you need to provide 2 arguments if you're using the method, and 3 if you're using the function:

`n`: The input value where `abs(n)` is between ~10<sup>-10<sup>308</sup></sup> and ~10<sup>10<sup>308</sup></sup> (for the stand-alone function),<br>
`s`: The input sign which can be either `1` (default) or `-1`<br>,
`form`: The input format which can be a string contained in the list: `["1", "1e1", "e1", "1e1e1", "e1e1", "1ee1", "ee1"]`<br>.

`n` and `s` are self-explanatory, so let's take a look at `form`.

Note: Formats do not support commas because I am too dumb to implement it efficiently.

Formats:

- `form = "1"`:
Displays the number as a raw string, with no formatting (e.g. 1e10000 would become a 1 with 10000 zeroes behind it). May be slightly inconsistent if `n` has a long decimal fraction.

- `form = "1e1"`:
Displays the number as a combination of `n`'s mantissa and exponent, without formatting the exponent (e.g. 1e10000000 would become 1e10000000).
If the number is between 1e-3 and 1e3, the exponent is hidden and instead the number is converted to be regular (e.g. 5e2 would become 500.00).
The exponent gets formatted if it's above 1e16 or below -1e4. This is due to python doing so at said thresholds, but the format strips the `+` sign.

- `form = "e1"`:
Integrates the mantissa into the exponent, without formatting it (e.g. 2e500 would become ~e500.301).
If the number is between 1e-3 and 1e3, similarly to `form = "1e1"`, the exponent is hidden and the number is displayed normally.

- `form = "1e1e1"` (default):
Same as `form = "1e1"`, except the exponent is formatted above 1e1e6 and below 1e-1e6, so 2e3000000, for example, would become 2.00e3.00e6.
If no format is given, the function defaults to this.

- `form = "e1e1"`:
Combination of `form = "e1"` and `form = 1e1e1`. 2e3000000 Would become ~e3000000.301, which would become ~e3.00e6.

- `form = "1ee1"`:
Same as `form = "1e1e1"`, except the exponent's mantissa is combined with the exponent, so 2e3000000 would become ~2ee6.477.

- `form = "ee1"`:
Combination of `form = "e1"` and `form = "1ee1"`. 2e3000000 would become ~ee6.477. The top exponent is technically different but at these magnitudes such differences are dwarfed by the rest of the number. Thus, the bottom mantissa is voided.

If the format is not specified, the function defaults to `form = "1e1e1"`.
If the sign is not specified, the function defaults to `1`.

Examples:

```python

disp(n, s, form) # Base function
self.disp(s, form) # Alternative form

x = Decimal("2e3000000")

print(disp(x, 1, "ee1")) # Output: ee6.48
print(disp(x, -1, "e1e1")) # Output: -e3.00e6
print(x.disp(1, "e1")) # Output: e3000000.30

x = Decimal("2e-3000000")

print(x.disp(1)) # Output: 2.00e-3.00e6
print(disp(x, -1, "1ee1")) # Output: -2.00ee-6.48

x = Decimal("-2e2")

print(disp(x)) # Output: -200.00
print(disp(x, -1)) # Output: 200.00

```

### Note:

The package also contains stand-alone functions, which can be called similarly to the methods, but you need to input an additional value in place of `self`.
e.g:

```python
x = Decimal("1e10000")

print(pow(x, 2)) # Returns "1e20000"
```

as opposed to:

```python
x = Decimal("1e10000")

print(x.pow(2)) # Returns "1e20000"
print(x ** 2) # Returns "1e20000"

x **= 2

print(x) # Returns "1e20000"
```

## Inputting values

As input for a `Decimal`, you can provide a `string`, `list`, `tuple`, `float` or `int` value, as well as other `Decimal` objects:

```python
print(Decimal("1e5000")) # 1.0e5000
print(Decimal(1.23456789)) # 1.23456789e0
print(Decimal(2510)) # 2.51e3
print(Decimal((2, 10))) # 2.0e10
print(Decimal([2, 11])) # 2.0e11
print(Decimal(Decimal("1e551"))) # 1.0e551
```

`Int` and `float` values can also be given as strings:

```python
print(Decimal("9835")) # 9.835e3
print(Decimal("9.87654321")) # 9.87654321e0
```

As both the `Decimal` class and its methods, along with all stand-alone functions normalize their input values,
the input rules for Decimals also apply to all functions.

A `Decimal` can be printed without `.disp(s)` or `disp(n, s)` to yield a basic visualization of the object:

```python

print(Decimal("1e2")) # 1e2
print(Decimal("1e10000")) # 1e10000
print(Decimal("1e1000000000")) # 1e1000000000, or 1e1e9

```

Visibly, the difference between simply printing `Decimal`s and using the `disp` functions is that,
when simply printing a Decimal, the exponent isn't formatted, and e notation is used for all values,
including, say, `1`, which would be turned into `1e0`, since `1 * 10^0 = 1 * 1 = 1`.

## Credits and license:

### Ideas:

https://github.com/Patashu/break_infinity.js:<br>
Amazing library which inspired both the name and functionality of this one, it's also a significant reason to why I made this.
Also because I wanted to rewrite my game Temporality's prototype's library, which was significantly limited compared to this one.

I may add the link to it here if I do make either the current version or perhaps the planned version available.

### License:

You can use this package in any way you want. You can make your own copies and distribute it, use it, etc.,
so long as you include the license of the package/project within your own copies if you do distribute it,
as per the MIT license.

For the full license please refer to the license at the top of the page.

## Version & Contribution:

### Version: V1.0.3

If you for some reason try this library out and find any issues, please don't hesitate to either report them as bugs,
or make a fork of the project to be used as a fix, and I'll check them out.

Please also let me know if you find there are functions not available as stand-alones.