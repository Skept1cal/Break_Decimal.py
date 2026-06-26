import math

# The Decimal class ----------------------------------------------------------------------------------------------------

class Decimal:

    """
    Python's double-precision floats cap out at ~1.797e308. In order to bypass this, we have to
    separate the mantissa from the exponent and perform arithmetic without directly evaluating their combination.

    The documentation of the normalize() function explains this in more detail.
    """

    def __init__(self, value):
        self.value = normalize(value)

    def __str__(self):
        return f"{self.value[0]}e{self.value[1]}"

    # Greater than (gt)

    '''We convert the values to their log10 equivalents in order to simplify all calculations here.'''

    def gt(self, other):
        return self.log10() > Decimal(other).log10()

    def __gt__(self, other):
        return self.gt(other)

    # Greater than or equal to (ge)

    def gte(self, other):
        return self.log10() >= Decimal(other).log10()

    def __ge__(self, other):
        return self.gte(other)

    # Less than (lt)

    def lt(self, other):
        return self.log10() < Decimal(other).log10()

    def __lt__(self, other):
        return self.lt(other)

    # Less than or equal to (le)

    def lte(self, other):
        return self.log10() <= Decimal(other).log10()

    def __le__(self, other):
        return self.lte(other)

    # Equal to (eq)

    def eq(self, other):
        return self.log10() == Decimal(other).log10()

    def __eq__(self, other):
        return self.eq(other)

    # Logarithms

    def log(self, base):

        """
        In order to compute a logarithm with base b,
        we have to multiply the exponent by logb(10), and add logb(a), where 'a' is the mantissa.

        To better understand this, let b = 2, and x (the Decimal value) = 1e10000.
        Now, since the exponent is in base 10, it scales with whatever power we must raise the input base to in order to get 10.
        In this case, we multiply the exponent by log2(10), which roughly equals 3.322.

        Additionally, we have to add the base b logarithm of the mantissa, or, in this case, log2(mantissa).
        It's important, though, that after this we also set the mantissa to 1, as we've already accounted for changing it when we evaluated the exponent.

        We can use this function to compute other logarithms, such as log2 or ln. The only exception to this is log10,
        as it is vastly simpler, both computationally and logically.

        Logarithms also take the absolute values of their input as negative numbers would result in complex values. 0 As an input is also undefined.

        This means that, except for subtraction, along with certain logarithm inputs, the value of a Decimal object is permanently locked to be positive,
        with the signage of the display functions only acting as a visual inversion if so desired, which CAN be linked to
        behaviours of numbers defined in the code using this module/package.
        """

        base = normalize(base)
        base = base[0] * 10 ** base[1]

        if base <= 0 or base == 1:
            raise ValueError(f"Invalid log base {base} is undefined.")
        
        if self.value[0] == 0:
            raise ValueError(f"Logarithm of zero is undefined.")

        return math.log(abs(self.value[0]), base) + self.value[1] * math.log(10, base)

    def log10(self):

        if self.value[0] == 0:
            raise ValueError(f"Logarithm of zero is undefined.")

        return math.log10(abs(self.value[0])) + self.value[1]

    def log2(self):
        return self.log(2)

    def ln(self):
        return self.log(math.e)

    # Power

    def pow(self, n):

        """
        In order to avoid overflowing with large powers, we have to convert the input value to its logarithmic form via the
        identity logb(x^n) = n * logb(x).

        We do this by thinking about the value as v = a * 10^b. Converting to a logarithmic form, this becomes
        log10(v) = log10(a) + b * log10(10), or log10(v) = log10(a) + b.
        We then multiply this logarithm by the power, since under these circumstances, exponentiation becomes multiplication,
        we can simply "raise" this value to n by multiplying it by n.

        After this, because we've already accounted for a's logarithmic form, we have to set a = 1,
        and then normalize a and b in order to get rid of the fractional exponent we will commonly get.
        """

        n = normalize(n)
        n = n[0] * 10 ** n[1]

        b = n * (self.value[1] + math.log10(self.value[0]))
        a = 1

        return Decimal((a, b))

    def __pow__(self, n):
        return self.pow(n)

    # Root

    def root(self, n):

        """
        The root is derived simply by raising the value to the power of the reciprocal of the root,
        as rootR(x) = x^(1/R).

        We will use similar logic to derive the inverse of other operations such as division and subtraction.
        """

        n = normalize(n)
        n = n[0] * 10 ** n[1]

        return self.pow(n ** -1)

    # Multiplication

    def mult(self, n):

        """
        Multiplication is done by multiplying the mantissas, and adding the exponents.

        The reason we are adding the exponents is because they are in logarithmic space (log10(1e10000) = 10000),
        in which multiplication becomes addition.
        """

        n = normalize(n)

        return Decimal((self.value[0] * n[0], self.value[1] + n[1]))

    def __mul__(self, n):
        return self.mult(n)

    # Division

    def div(self, n):

        """
        As mentioned above, we can simply derive the division by multiplying the input value by the reciprocal of the input denominator.
        """

        n = normalize(n)
        if n[0] == 0:
            raise ZeroDivisionError("Division by zero is undefined.")
        return self.mult(Decimal(n).pow(-1))

    def __truediv__(self, n):
        return self.div(n)

    # Addition

    def add(self, n):

        """
        In order to perform addition, we have to scale the mantissa of the smaller number in order to make the exponents equal,
        after which we can perform addition on the mantissas.
        This value needs to be normalized in case the sum exceeds 10 or is under 1,
        which is already handled by returning the value as a new Decimal class.

        Additionally, if the difference in exponents is too large (|exp1 - exp2| > 15),
        we can simply return the value of the greater input value, as the difference from the addition would be negligible.
        """

        n = normalize(n)

        if abs(self.value[1] - n[1]) > 15:
            return Decimal(bigmax(self, n))

        scaling = abs(self.value[1] - n[1])

        if self.gte(n):
            a = self.value[0] + n[0] / 10 ** scaling
            b = self.value[1] # 'b' doesn't have to be adjusted as 'a' will remain between 1 and 10 due to the scaling. Any potential edge-cases are handled by returning a normalized/Decimal object.

            return Decimal((a, b))
        else:
            a = n[0] + self.value[0] / 10 ** scaling
            b = n[1]

            return Decimal((a, b))

    def __add__(self, n):
        return self.add(n)

    # Subtraction method

    def sub(self, n):

        """
        Again, we can simply derive subtraction from adding the first input value and the negative of the second.
        This way, we are performing subtraction as x + -y.
        """

        return self.add(mult(n, -1))

    def __sub__(self, n):
        return self.sub(n)

    # Display

    def disp(self, s):

        """
        In order to display the value of the object, we default to some arbitrary transition point between standard values and scientific notation.
        We also take an input value for the sign in order to specify if the displayed number should be positive or negative.
        This can be replaced with one's own display function if desired.

        This function also displays the exponent in scientific form (turning the format into x * 10^(y * 10^z)),
        making it more easily legible. Again, this can be replaced with one's own display function if desired.
        """

        if s not in [-1, 1]:
            raise ValueError(f"Invalid value for 's'; expected: {[-1, 1]}, got: {s}")

        if self.value[0] == 0:
            return f"{0:.2f}"

        if -3 < self.log10() < 3:
            return f"{(self.value[0] * s) * 10 ** self.value[1]:.2f}"
        elif -1e6 < self.value[1] < 1e6:
            return f"{self.value[0] * s:.2f}e{self.value[1]}"
        else:

            exp_mantissa = 10 ** (math.log10(abs(self.value[1])) - math.log10(abs(self.value[1])) // 1)
            exp_exponent = int(math.log10(abs(self.value[1])))
            exp_sign = -1 if self.value[1] < 0 else 1

            return f"{self.value[0] * s:.2f}e{exp_sign * exp_mantissa:.2f}e{exp_exponent}"

# Stand-alone functions ------------------------------------------------------------------------------------------------

# Normalization

def normalize(x : Decimal | str | tuple | list | int | float):

    """
    In Python, and other languages, a standard double-precision float can represent values roughly between 1e308 and 1e-308.

    In order to bypass this, we must separate the mantissa (a) from the exponent (b) in the equation n = a * 10^b,
    where 1 <= a < 10, and b is a whole number.

    As such, if either a < 1 or a > 10 is true, the values should be normalized.
    If a = 0, we can skip everything as x * 0 = 0.

    If 'b', the exponent, has a fractional part (f), we should also multiply 'a', the mantissa by 10^f.

    All of this allows us to represent numbers up to roughly 10^10^308, 1e1e308, or 1ee308,
    as the exponent itself has now become the limiting factor.

    In order to receive strings as values, we look for an "e" in the input,
    and if we can find it, we assign the left side of it to 'a' (the mantissa), and the right side to 'b' (the exponent).
    If we cannot find it, we assume the number to be a standard int/float and convert it to the separated format.
    In the case that "e" is present in the input, we execute the steps detailed above in order to get a normalized value.

    We can apply similar logic to tuple, list, int, float or Decimal object inputs.
    """

    # Handling string input

    if type(x) == str:  # e.g. "1e500", "1e-3000"
        if "e" in x.lower():
            # Extracting 'a' and 'b' from 'x'
            index = x.index("e")
            a = float(x[:index])
            b = float(x[index + 1:])

            if a == 0:
                return 0, 0

            # Scaling 'a' and 'b'
            scaling = math.floor(math.log10(abs(a)))

            a /= 10 ** scaling
            b += scaling

            if type(b) == float:
                a *= 10 ** (b - int(b))

                scaling = math.floor(math.log10(abs(a)))
                a, b = a / 10 ** scaling, int(b + scaling)

            return a, int(b)
        else:
            scaling = math.floor(math.log10(abs(float(x))))

            a = float(x) / 10 ** scaling
            b = scaling

        return a, int(b)

    # Handling tuple/list input

    elif type(x) == tuple or type(x) == list: # e.g. (1, 500), [1, -3000]
        if x[0] == 0:
            return 0, 0

        scaling = math.floor(math.log10(abs(x[0])))

        a = x[0] / 10 ** scaling
        b = x[1] + scaling

        if type(b) == float:
            a *= 10 ** (b - int(b))

            scaling = math.floor(math.log10(abs(a)))
            a, b = a / 10 ** scaling, int(b + scaling)

        return a, int(b)

    # Handling Decimal class input

    elif type(x) == Decimal:
        if x.value[0] == 0:
            return 0, 0

        scaling = math.floor(math.log10(abs(x.value[0])))

        a = x.value[0] / 10 ** scaling
        b = x.value[1] + scaling

        if type(b) == float:
            a *= 10 ** (b - int(b))

            scaling = math.floor(math.log10(abs(a)))
            a, b = a / 10 ** scaling, int(b + scaling)

        return a, int(b)

    # Handling int/float input

    elif type(x) == int or type(x) == float: # e.g. 1.797e308, -179700000000000000000000...0
        if x == 0:
            return 0, 0

        scaling = math.floor(math.log10(abs(x)))

        a = x / 10 ** scaling
        b = scaling

        return (a, int(b)) if a != 0 else (0, 0)

    else:
        raise TypeError(f"Invalid input type for function normalize()\nExpected: {["str", "int", "float", "tuple", "list", "Decimal"]}, got: {type(x)}")

# Min/max

def bigmax(n1, n2):
    return Decimal(n1) if Decimal(n1).log10() >= Decimal(n2).log10() else Decimal(n2) # 'n1' takes priority in the case of equality. This doesn't matter because n1 = n2.

def bigmin(n1, n2):
    return Decimal(n1) if Decimal(n1).log10() <= Decimal(n2).log10() else Decimal(n2)

# Inequality functions

def gt(n1, n2):
    return log10(n1) > log10(n2)

def gte(n1, n2):
    return log10(n1) >= log10(n2)

def lt(n1, n2):
    return log10(n1) < log10(n2)

def lte(n1, n2):
    return log10(n1) <= log10(n2)

def eq(n1, n2):
    return log10(n1) == log10(n2)

# Logarithm functions

def log(n, base):
    base = normalize(base)
    base = base[0] * 10 ** base[1]

    if base <= 0 or base == 1:
        raise ValueError(f"Invalid log base {base} is undefined.")

    n = normalize(n)

    if n[0] == 0:
        raise ValueError(f"Logarithm of zero is undefined.")

    return math.log(abs(n[0], base)) + n[1] * math.log(10, base)

def log10(n):
    n = normalize(n)

    if n[0] == 0:
        raise ValueError(f"Logarithm of zero is undefined.")

    return math.log10(abs(n[0])) + n[1]

def log2(n):
    n = normalize(n)
    return log(n, 2)

def ln(n):
    return log(n, math.e)

# Power and root functions

def pow(base, exp):
    exp = normalize(exp)
    exp = exp[0] * 10 ** exp[1]

    if exp == 0:
        return Decimal(1)

    base = normalize(base)

    b = exp * (base[1] + math.log10(base[0]))
    a = 1

    return Decimal(normalize((a, b)))

def root(base, root):
    root = normalize(root)
    root = root[0] * 10 ** root[1]

    return pow(base, root ** -1)

# Multiplication and division functions

def mult(a, b):
    b = normalize(b)
    a = normalize(a)

    return Decimal((a[0] * b[0], a[1] + b[1]))

def div(a, b):
    return mult(a, pow(b, -1))

# Addition and subtraction functions

def add(n1, n2):
    n2 = normalize(n2)
    n1 = normalize(n1)

    if abs(n1[1] - n2[1]) > 15:
        return Decimal(bigmax(n1, n2))

    scaling = abs(n1[1] - n2[1])

    if gte(n1, n2):
        a = n1[0] + n2[0] / 10 ** scaling
        b = n1[1] # 'b' doesn't have to be adjusted as 'a' will remain between 1 and 10 due to the scaling. Any potential edge-cases are handled by returning a normalized/Decimal object.
    else:
        a = n2[0] + n1[0] / 10 ** scaling
        b = n2[1]
    
    return Decimal((a, b))

def sub(n1, n2):
    return add(n1, mult(n2, -1))

# Display function -----------------------------------------------------------------------------------------------------

def disp(n, s):

    n = normalize(n)

    if s not in [-1, 1]:
        raise ValueError(f"Invalid value for 's'; expected: {[-1, 1]}, got: {s}")

    if n[0] == 0:
        return f"{0:.2f}"

    if -3 < log10(n) < 3:
        return f"{(n[0] * s) * 10 ** n[1]:.2f}"
    elif -1e6 < n[1] < 1e6:
        return f"{n[0] * s:.2f}e{n[1]}"
    else:

        exp_mantissa = 10 ** (math.log10(abs(n[1])) - math.log10(abs(n[1])) // 1)
        exp_exponent = int(math.log10(abs(n[1])))
        exp_sign = -1 if n[1] < 0 else 1

        return f"{n[0] * s:.2f}e{exp_sign * exp_mantissa:.2f}e{exp_exponent}"