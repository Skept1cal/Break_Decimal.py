A numerical library for Python, largely inspired by https://github.com/Patashu/break_infinity.js.

This library can work with and represent values up to around ~1ee308 (10<sup>10<sup>308</sup></sup>), as opposed to standard floats which cap out at ~1.797e308.

## Importing

In order to use the package, you must install it on your computer with:

```
pip install git+https://github.com/Skept1cal/Break_Decimal.py
```

Then, you can import it into any project through:

```
from Break_Decimal import Decimal
```

or:

```
import Break_Decimal as breakdec
```

## Functions

# Unique stand-alones

```Decimal``` - Creates a Decimal class object with tuple attribute *value*
normalize(x)/norm(x) - Normalizes input value *x* into a *tuple* representing the standard form *a * 10<sup>b</sup>*
bigmax(n1, n2) - Returns the **greater** value out of *n1* and *n2*
bigmin(n1, n2) - Returns the **smaller** value out of *n1* and *n2*

# Methods

self.gt(other)/*self* > *other* - Returns boolean based on whether *self* > *other* is true
self.gte(other)/*self* >= *other* - Returns boolean based on whether *self* >= *other* is true
self.lt(other)/*self* < *other* - Returns boolean based on whether *self* < *other* is true
self.lte(other)/*self* <= *other* - Returns boolean based on whether *self* <= *other* is true
self.eq(other)/*self* == *other* - Returns boolean based on whether *self* == *other* is true

***NOTE: LOGARITHMS DO NOT TAKE NEGATIVE VALUES.***

self.log(base) - Returns log*base* of *self*
self.log10() - Returns log*10* of *self*
self.log2() - Returns log*2* of *self*
self.ln() - Returns the natural logarithm (~2.71828) of *self*

self.pow(n)/*self* ** *n* - Returns _self ** n_
self.root(n) - Returns the *n*th root of *self*. Alternatively, you can call _self.pow(n ** -1)_ to calculate roots. Be mindful of *n*'s type.

self.mult(n)/self.mul(n)/*self* * *n* - Returns *self * n*
self.div(n)/*self* / *n* - Returns *self / n*

self.add(n)/*self* + *n* - Returns *self + n*
self.sub(n)/*self* - *n* - Returns *self - n*

self.disp(s) - Returns a built-in display format for *self*, with *sign (s)*. *s* can be either *1* or *-1*, other values will raise a *ValueError*.
If the exponent of *self* (or *self.log10()*) is between *-3* and *3*, e notation is not used.
If the exponent of *self* (or *self.log10()*) is between *-1e6* and *-3*, or *3* and *1e6* singular e notation is used.
if the exponent of *self* (or *self.log10()*) is below *-1e6* or above *1e6*, e notation is used on the exponent as well.
e.g:

```
print(Decimal("1e1").disp(1)) # Returns "10.00"
print(Decimal("1e100").disp(-1)) # Returns "-1.00e100"
print(Decimal("1e10000000").disp(1)) # Returns "1.00e1.00e7"
print(Decimal("1e-2").disp(1)) # Returns "0.01"
```

# Note:

The package also contains stand-alone functions, which can be called similarly to the methods, but you need to input an additional value in place of *self*.
e.g:

```
x = Decimal("1e10000")

print(pow(x, 2)) # Returns "1e20000"
```

as opposed to:

```
x = Decimal("1e10000")

print(x.pow(2)) # Returns "1e20000"
print(x ** 2) # Returns "1e20000"

x **= 2

print(x) # Returns "1e20000"
```

## Inputting values

As input for a Decimal, you can provide a string, list, tuple, float or int value, as well as other Decimal objects:

```
print(Decimal("1e5000")) # 1.0e5000
print(Decimal(1.23456789)) # 1.23456789e0
print(Decimal(2510)) # 2.51e3
print(Decimal((2, 10))) # 2.0e10
print(Decimal([2, 11])) # 2.0e11
print(Decimal(Decimal("1e551"))) # 1.0e551
```

Int and float values can also be given as strings:

```
print(Decimal("9835")) # 9.835e3
print(Decimal("9.87654321")) # 9.87654321e0
```

As both the Decimal class and its methods, along with all stand-alone functions normalize their input values,
the input rules for Decimals also apply to all functions.

A Decimal can be printed without *.disp(s)* or *disp(n, s*) to yield a basic visualization of the object:

```
print(Decimal("1e10000")) # 1e10000
print(Decimal("1e1000000000)) # 1e1000000000, or 1e1e9
```

Visibly, the difference between simply printing Decimals and using the display functions is that,
when simply printing the object, the exponent isn't formatted, and e notation is used for all values,
including, say, *1*, which would be turned into *1e0 (1 * 10^0 = 1 * 1 = 1)*.

## Credits and license

# Ideas:

https://github.com/Patashu/break_infinity.js
Amazing library which inspired both the name and functionality of this one, it's also a significant reason to why I made this.
Also because I wanted to rewrite my game Temporality's prototype's library, which was significantly limited compared to this one.

You can check out the game here:
*placeholder text*

# License:

You can use this package in any way you want. You can make your own copies and distribute it, use it, etc.,
so long as you include the license of the package/project within your own copies if you do distribute it,
as per the MIT license.

For the full license refer to the license at the top of the page.