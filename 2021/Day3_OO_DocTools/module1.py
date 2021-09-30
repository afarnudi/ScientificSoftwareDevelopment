"""Random variable generators.

    integers
    --------
           uniform within range

    sequences
    ---------
           pick random element
           pick random sample
           pick weighted random sample
           generate random permutation

    distributions on the real line:
    -------------------------------
           uniform
           triangular
           normal (Gaussian)
           lognormal
           negative exponential
           gamma
           beta
           pareto
           Weibull

    distributions on the circle (angles 0 to 2pi)
    ---------------------------------------------
           circular uniform
           von Mises

General notes on the underlying Mersenne Twister core generator:

* The period is 2**19937-1.
* It is one of the most extensively tested generators in existence.
* The random() method is implemented in C, executes in a single Python step,
  and is, therefore, threadsafe.

"""

from warnings import warn as _warn
from types import MethodType as _MethodType, BuiltinMethodType as _BuiltinMethodType
from math import log as _log, exp as _exp, pi as _pi, e as _e, ceil as _ceil
from math import sqrt as _sqrt, acos as _acos, cos as _cos, sin as _sin
from os import urandom as _urandom
from _collections_abc import Set as _Set, Sequence as _Sequence
from hashlib import sha512 as _sha512
import itertools as _itertools
import bisect as _bisect
import os as _os

__all__ = ["Random","seed","random","uniform","randint","choice","sample",
           "randrange","shuffle","normalvariate","lognormvariate",
           "expovariate","vonmisesvariate","gammavariate","triangular",
           "gauss","betavariate","paretovariate","weibullvariate",
           "getstate","setstate", "getrandbits", "choices",
           "SystemRandom"]

NV_MAGICCONST = 4 * _exp(-0.5)/_sqrt(2.0)
TWOPI = 2.0*_pi
LOG4 = _log(4.0)
SG_MAGICCONST = 1.0 + _log(4.5)
BPF = 53        # Number of bits in a float
RECIP_BPF = 2**-BPF


# Translated by Guido van Rossum from C source provided by
# Adrian Baddeley.  Adapted by Raymond Hettinger for use with
# the Mersenne Twister  and os.urandom() core generators.

import _random

class Random(_random.Random):
    """Random number generator base class used by bound module functions.

    Used to instantiate instances of Random to get generators that don't
    share state.

    Class Random can also be subclassed if you want to use a different basic
    generator of your own devising: in that case, override the following
    methods:  random(), seed(), getstate(), and setstate().
    Optionally, implement a getrandbits() method so that randrange()
    can cover arbitrarily large ranges.

    """

    VERSION = 3     # used by getstate/setstate

    def __init__(self, x=None):
        """Initialize an instance.

        Optional argument x controls seeding, as for Random.seed().
        """

        self.seed(x)
        self.gauss_next = None

    def seed(self, a=None, version=2):
        """Initialize internal state from hashable object.

        None or no argument seeds from current time or from an operating
        system specific randomness source if available.

        If *a* is an int, all bits are used.

        For version 2 (the default), all of the bits are used if *a* is a str,
        bytes, or bytearray.  For version 1 (provided for reproducing random
        sequences from older versions of Python), the algorithm for str and
        bytes generates a narrower range of seeds.

        """

        if version == 1 and isinstance(a, (str, bytes)):
            a = a.decode('latin-1') if isinstance(a, bytes) else a
            x = ord(a[0]) << 7 if a else 0
            for c in map(ord, a):
                x = ((1000003 * x) ^ c) & 0xFFFFFFFFFFFFFFFF
            x ^= len(a)
            a = -2 if x == -1 else x

        if version == 2 and isinstance(a, (str, bytes, bytearray)):
            if isinstance(a, str):
                a = a.encode()
            a += _sha512(a).digest()
            a = int.from_bytes(a, 'big')

        super().seed(a)
        self.gauss_next = None

    def getstate(self):
        """Return internal state; can be passed to setstate() later."""
        return self.VERSION, super().getstate(), self.gauss_next

    def setstate(self, state):
        """Restore internal state from object returned by getstate()."""
        version = state[0]
        if version == 3:
            version, internalstate, self.gauss_next = state
            super().setstate(internalstate)
        elif version == 2:
            version, internalstate, self.gauss_next = state
            # In version 2, the state was saved as signed ints, which causes
            #   inconsistencies between 32/64-bit systems. The state is
            #   really unsigned 32-bit ints, so we convert negative ints from
            #   version 2 to positive longs for version 3.
            try:
                internalstate = tuple(x % (2**32) for x in internalstate)
            except ValueError as e:
                raise TypeError from e
            super().setstate(internalstate)
        else:
            raise ValueError("state with version %s passed to "
                             "Random.setstate() of version %s" %
                             (version, self.VERSION))

## ---- Methods below this point do not need to be overridden when
## ---- subclassing for the purpose of using a different core generator.

## -------------------- pickle support  -------------------

    # Issue 17489: Since __reduce__ was defined to fix #759889 this is no
    # longer called; we leave it here because it has been here since random was
    # rewritten back in 2001 and why risk breaking something.
    def __getstate__(self): # for pickle
        return self.getstate()

    def __setstate__(self, state):  # for pickle
        self.setstate(state)

    def __reduce__(self):
        return self.__class__, (), self.getstate()

## -------------------- integer methods  -------------------

    def randrange(self, start, stop=None, step=1, _int=int):
        """Choose a random item from range(start, stop[, step]).

        This fixes the problem with randint() which includes the
        endpoint; in Python this is usually not what you want.

        """

        # This code is a bit messy to make it fast for the
        # common case while still doing adequate error checking.
        istart = _int(start)
        if istart != start:
            raise ValueError("non-integer arg 1 for randrange()")
        if stop is None:
            if istart > 0:
                return self._randbelow(istart)
            raise ValueError("empty range for randrange()")

        # stop argument supplied.
        istop = _int(stop)
        if istop != stop:
            raise ValueError("non-integer stop for randrange()")
        width = istop - istart
        if step == 1 and width > 0:
            return istart + self._randbelow(width)
        if step == 1:
            raise ValueError("empty range for randrange() (%d,%d, %d)" % (istart, istop, width))

        # Non-unit step argument supplied.
        istep = _int(step)
        if istep != step:
            raise ValueError("non-integer step for randrange()")
        if istep > 0:
            n = (width + istep - 1) // istep
        elif istep < 0:
            n = (width + istep + 1) // istep
        else:
            raise ValueError("zero step for randrange()")

        if n <= 0:
            raise ValueError("empty range for randrange()")

        return istart + istep*self._randbelow(n)

    def randint(self, a, b):
        """Return random integer in range [a, b], including both end points.
        """

        return self.randrange(a, b+1)

    def _randbelow(self, n, int=int, maxsize=1<<BPF, type=type,
                   Method=_MethodType, BuiltinMethod=_BuiltinMethodType):
        "Return a random int in the range [0,n).  Raises ValueError if n==0."

        random = self.random
        getrandbits = self.getrandbits
        # Only call self.getrandbits if the original random() builtin method
        # has not been overridden or if a new getrandbits() was supplied.
        if type(random) is BuiltinMethod or type(getrandbits) is Method:
            k = n.bit_length()  # don't use (n-1) here because n can be 1
            r = getrandbits(k)          # 0 <= r < 2**k
            while r >= n:
                r = getrandbits(k)
            return r
        # There's an overridden random() method but no new getrandbits() method,
        # so we can only use random() from here.
        if n >= maxsize:
            _warn("Underlying random() generator does not supply \n"
                "enough bits to choose from a population range this large.\n"
                "To remove the range limitation, add a getrandbits() method.")
            return int(random() * n)
        if n == 0:
            raise ValueError("Boundary cannot be zero")
        rem = maxsize % n
        limit = (maxsize - rem) / maxsize   # int(limit * maxsize) % n == 0
        r = random()
        while r >= limit:
            r = random()
        return int(r*maxsize) % n

## -------------------- sequence methods  -------------------

    def choice(self, seq):
        """Choose a random element from a non-empty sequence."""
        try:
            i = self._randbelow(len(seq))
        except ValueError:
            raise IndexError('Cannot choose from an empty sequence') from None
        return seq[i]

    def shuffle(self, x, random=None):
        """Shuffle list x in place, and return None.

        Optional argument random is a 0-argument function returning a
        random float in [0.0, 1.0); if it is the default None, the
        standard random.random will be used.

        """

        if random is None:
            randbelow = self._randbelow
            for i in reversed(range(1, len(x))):
                # pick an element in x[:i+1] with which to exchange x[i]
                j = randbelow(i+1)
                x[i], x[j] = x[j], x[i]
        else:
            _int = int
            for i in reversed(range(1, len(x))):
                # pick an element in x[:i+1] with which to exchange x[i]
                j = _int(random() * (i+1))
                x[i], x[j] = x[j], x[i]

    def sample(self, population, k):
        """Chooses k unique random elements from a population sequence or set.

        Returns a new list containing elements from the population while
        leaving the original population unchanged.  The resulting list is
        in selection order so that all sub-slices will also be valid random
        samples.  This allows raffle winners (the sample) to be partitioned
        into grand prize and second place winners (the subslices).

        Members of the population need not be hashable or unique.  If the
        population contains repeats, then each occurrence is a possible
        selection in the sample.

        To choose a sample in a range of integers, use range as an argument.
        This is especially fast and space efficient for sampling from a
        large population:   sample(range(10000000), 60)
        """

        # Sampling without replacement entails tracking either potential
        # selections (the pool) in a list or previous selections in a set.

        # When the number of selections is small compared to the
        # population, then tracking selections is efficient, requiring
        # only a small set and an occasional reselection.  For
        # a larger number of selections, the pool tracking method is
        # preferred since the list takes less space than the
        # set and it doesn't suffer from frequent reselections.

        if isinstance(population, _Set):
            population = tuple(population)
        if not isinstance(population, _Sequence):
            raise TypeError("Population must be a sequence or set.  For dicts, use list(d).")
        randbelow = self._randbelow
        n = len(population)
        if not 0 <= k <= n:
            raise ValueError("Sample larger than population or is negative")
        result = [None] * k
        setsize = 21        # size of a small set minus size of an empty list
        if k > 5:
            setsize += 4 ** _ceil(_log(k * 3, 4)) # table size for big sets
        if n <= setsize:
            # An n-length list is smaller than a k-length set
            pool = list(population)
            for i in range(k):         # invariant:  non-selected at [0,n-i)
                j = randbelow(n-i)
                result[i] = pool[j]
                pool[j] = pool[n-i-1]   # move non-selected item into vacancy
        else:
            selected = set()
            selected_add = selected.add
            for i in range(k):
                j = randbelow(n)
                while j in selected:
                    j = randbelow(n)
                selected_add(j)
                result[i] = population[j]
        return result

    def choices(self, population, weights=None, *, cum_weights=None, k=1):
        """Return a k sized list of population elements chosen with replacement.

        If the relative weights or cumulative weights are not specified,
        the selections are made with equal probability.

        """
        random = self.random
        if cum_weights is None:
            if weights is None:
                _int = int
                total = len(population)
                return [population[_int(random() * total)] for i in range(k)]
            cum_weights = list(_itertools.accumulate(weights))
        elif weights is not None:
            raise TypeError('Cannot specify both weights and cumulative weights')
        if len(cum_weights) != len(population):
            raise ValueError('The number of weights does not match the population')
        bisect = _bisect.bisect
        total = cum_weights[-1]
        hi = len(cum_weights) - 1
        return [population[bisect(cum_weights, random() * total, 0, hi)]
                for i in range(k)]

## -------------------- real-valued distributions  -------------------

## -------------------- uniform distribution -------------------

    def uniform(self, a, b):
        "Get a random number in the range [a, b) or [a, b] depending on rounding."
        return a + (b-a) * self.random()

## -------------------- triangular --------------------

    def triangular(self, low=0.0, high=1.0, mode=None):
        """Triangular distribution.

        Continuous distribution bounded by given lower and upper limits,
        and having a given mode value in-between.

        http://en.wikipedia.org/wiki/Triangular_distribution

        """
        u = self.random()
        try:
            c = 0.5 if mode is None else (mode - low) / (high - low)
        except ZeroDivisionError:
            return low
        if u > c:
            u = 1.0 - u
            c = 1.0 - c
            low, high = high, low
        return low + (high - low) * _sqrt(u * c)

## -------------------- normal distribution --------------------

    def normalvariate(self, mu, sigma):
        """Normal distribution.

        mu is the mean, and sigma is the standard deviation.

        """
        # mu = mean, sigma = standard deviation

        # Uses Kinderman and Monahan method. Reference: Kinderman,
        # A.J. and Monahan, J.F., "Computer generation of random
        # variables using the ratio of uniform deviates", ACM Trans
        # Math Software, 3, (1977), pp257-260.

        random = self.random
        while 1:
            u1 = random()
            u2 = 1.0 - random()
            z = NV_MAGICCONST*(u1-0.5)/u2
            zz = z*z/4.0
            if zz <= -_log(u2):
                break
        return mu + z*sigma
