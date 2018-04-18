from __future__ import division
import numpy as np
import gmpy2
from gmpy2 import mpz
from numba import jit
import os
import sys

def _generate_const_seq(N):
    return np.zeros(N, dtype='uint8')


def generate_const_seq(N, seq):
    M = N - len(seq)
    if M > 0:
        buf = _generate_const_seq(M)
        seq = np.concatenate([seq, buf]).astype('uint8')
    else:
        seq = seq[:N]
    assert len(seq) == N
    return seq


def _generate_checkerboard_seq(N):
    seq = np.zeros(N, dtype='uint8')
    seq[::2] = 1
    return seq


def generate_checkerboard_seq(N, seq):
    Nold = len(seq)
    M = N - Nold
    if M > 0:
        buf = _generate_const_seq(M)
        seq = np.concatenate([seq, buf]).astype('uint8')
        m = Nold - 1 if Nold % 2 else Nold
        seq[m::2] = 1
    else:
        seq = seq[:N]
    assert len(seq) == N
    return seq


def _generate_random_seq(N):
    return np.random.randint(0, 2, N, dtype='uint8')


def generate_random_seq(N, seq):
    M = N - len(seq)
    if M > 0:
        buf = _generate_random_seq(M)
        seq = np.concatenate([seq, buf]).astype('uint8')
    else:
        seq = seq[:N]
    assert len(seq) == N
    return seq


def _binary(n):
    """
     return binary representation of a number
    """
    return np.array([a for a in str(bin(n))[2:]], dtype='int')


def _generate_rudin_shapiro_seq(N, Nstart=0):
    an = []
    for n in range(Nstart, N):
        nbin = _binary(n)
        bn = np.sum(nbin[:-1] * nbin[1:]).astype('int')
        an.append(np.power(-1, bn))
    an = np.asarray(an, dtype='int8')
    an[an < 0] = 0
    return np.asarray(an, dtype='uint8')


def generate_rudin_shapiro_seq(N, seq):
    M = N - len(seq)
    if M > 0:
        buf = _generate_rudin_shapiro_seq(N, Nstart=len(seq))
        seq = np.concatenate([seq, buf]).astype('uint8')
    else:
        seq = seq[:N]
    assert len(seq) == N
    return seq


def _generate_thue_morse_seq(N, Nstart=0):
    f = lambda n: bin(n).count('1') % 2
    return np.array([f(n) for n in range(Nstart, N)], dtype='uint8')


def generate_thue_morse_seq(N, seq):
    M = N - len(seq)
    if M > 0:
        buf = _generate_thue_morse_seq(N, Nstart=len(seq))
        seq = np.concatenate([seq, buf]).astype('uint8')
    else:
        seq = seq[:N]
    assert len(seq) == N
    return seq


def _generate_fibonacci_seq(N, Nstart=0):
    tau = (1. + np.sqrt(5)) / 2.
    f = lambda n: 2 + np.floor(n * tau) - np.floor((n + 1.) * tau)
    return np.array([f(n) for n in range(Nstart + 1, N + 1)], dtype='uint8')


def generate_fibonacci_seq(N, seq):
    M = N - len(seq)
    if M > 0:
        buf = _generate_fibonacci_seq(N, Nstart=len(seq))
        seq = np.concatenate([seq, buf]).astype('uint8')
    else:
        seq = seq[:N]
    assert len(seq) == N
    return seq


@jit
def _kolakoski():
    # from https://oeis.org/A000002
    # http://11011110.livejournal.com/336374.html
    x = y = -1
    while True:
        yield [2, 1][x & 1]
        f = y & ~ (y + 1)
        x ^= f
        y = (y + 1) | (f & (x >> 1))


def _generate_kolakoski_seq(N):
    K = _kolakoski()
    a = np.array([K.next() for _ in range(N)], dtype='uint8')
    a[a > 1] = 0
    return a


def generate_kolakoski_seq(N, seq):
    # not sure how to restart this from len(seq)
    return _generate_kolakoski_seq(N)


def _generate_baum_sweet_seq(N, Nstart=0):
    """
    https://oeis.org/A086747
    http://mathworld.wolfram.com/Baum-SweetSequence.html
    """
    if Nstart == 0:
        seq = [1]
        Nstart += 1
    else:
        seq = []
    #seq.extend([0 if '0' in `bin(n)[2:].split('00')` else 1 for n in range(Nstart, N)])
    seq.extend([0 if '0' in bin(n)[2:].split('00') else 1 for n in range(Nstart, N)])
    return seq


def generate_baum_sweet_seq(N, seq):
    M = N - len(seq)
    if M > 0:
        buf = _generate_baum_sweet_seq(N, Nstart=len(seq))
        seq = np.concatenate([seq, buf]).astype('uint8')
    else:
        seq = seq[:N]
    assert len(seq) == N
    return seq


def _generate_dragon_seq(N, Nstart=0):
    """
    https://oeis.org/A014577
    https://codegolf.stackexchange.com/questions/128858/the-dragon-curve-sequence/128865
    """
    f = lambda n: n & -n & n // 2 < 1
    return np.array([f(n) for n in range(Nstart + 1, N + 1)], dtype='uint8')


def generate_dragon_seq(N, seq):
    M = N - len(seq)
    if M > 0:
        buf = _generate_dragon_seq(N, Nstart=len(seq))
        seq = np.concatenate([seq, buf]).astype('uint8')
    else:
        seq = seq[:N]
    assert len(seq) == N
    return seq


def _generate_ehrenfeucht_mycielski_seq(N, Nstart=0):
    """
    https://oeis.org/A038219
    file can be downloaded at http://barnyard.syr.edu/mseq/mseq.shtml
    """
    assert N < 1e6
    path = os.path.join(os.path.dirname(__file__), 'mseq.1000k.txt')
    seq = []
    i = 0
    with open(path) as fileobj:
        for line in fileobj:
            for ch in line.strip():
                if i > N:
                    return np.array(seq, dtype='uint8')
                elif i > Nstart:
                    seq.append(int(ch))
                i += 1
    return np.array(seq, dtype='uint8')


def generate_ehrenfeucht_mycielski_seq(N, seq):
    M = N - len(seq)
    if M > 0:
        buf = _generate_ehrenfeucht_mycielski_seq(N, Nstart=len(seq))
        seq = np.concatenate([seq, buf]).astype('uint8')
    else:
        seq = seq[:N]
    assert len(seq) == N
    return seq


def pi_chudnovsky_bs(ndigits):
    """
    https://superuser.com/questions/3810/where-to-download-a-lot-of-digits-of-pi
    
    Compute int(pi * 10**ndigits)
    This is done using Chudnovsky's series with binary splitting
    """
    C = 640320
    C3_OVER_24 = C ** 3 // 24

    def bs(a, b):
        """
        Computes the terms for binary splitting the Chudnovsky infinite series
        a(a) = +/- (13591409 + 545140134*a)
        p(a) = (6*a-5)*(2*a-1)*(6*a-1)
        b(a) = 1
        q(a) = a*a*a*C3_OVER_24
        returns P(a,b), Q(a,b) and T(a,b)
        """
        if b - a == 1:
            # Directly compute P(a,a+1), Q(a,a+1) and T(a,a+1)
            if a == 0:
                Pab = Qab = mpz(1)
            else:
                Pab = mpz((6 * a - 5) * (2 * a - 1) * (6 * a - 1))
                Qab = mpz(a * a * a * C3_OVER_24)
            Tab = Pab * (13591409 + 545140134 * a)  # a(a) * p(a)
            if a & 1:
                Tab = -Tab
        else:
            # Recursively compute P(a,b), Q(a,b) and T(a,b)
            # m is the midpoint of a and b
            m = (a + b) // 2
            # Recursively calculate P(a,m), Q(a,m) and T(a,m)
            Pam, Qam, Tam = bs(a, m)
            # Recursively calculate P(m,b), Q(m,b) and T(m,b)
            Pmb, Qmb, Tmb = bs(m, b)
            # Now combine
            Pab = Pam * Pmb
            Qab = Qam * Qmb
            Tab = Qmb * Tam + Pam * Tmb
        return Pab, Qab, Tab

    # how many terms to compute
    DIGITS_PER_TERM = np.log10(C3_OVER_24 / 6 / 2 / 6)
    N = int(ndigits / DIGITS_PER_TERM + 1)
    # Calclate P(0,N) and Q(0,N)
    P, Q, T = bs(0, N)
    one_squared = mpz(10) ** (2 * ndigits)
    # sqrtC = (10005*one_squared).sqrt()
    sqrtC = gmpy2.isqrt(10005 * one_squared)
    return (Q * 426880 * sqrtC) // T


def generate_pi_seq(N, Nstart=0): # map: maps a function to a sequence
    #return np.array(map(int, pi_chudnovsky_bs(N).__str__())[Nstart:N], dtype='uint8')
    return np.array(map(int, pi_chudnovsky_bs(N).__str__()[Nstart:N]), dtype='uint8')

def generate_checker_2d(width, nfields):
    nfields = nfields / 2
    np.kron([[1, 0] * nfields, [0, 1] * nfields] * nfields, np.ones((width, width)))


def printOut(toFile, text):
    if os.path.exists(toFile):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not
    with open(toFile, append_write,encoding= 'utf-8') as f:
        #text = text.encode('utf-8', 'replace')
        #print(" i am here")
        #print(type(text))
        f.write(text)
        # #print(text, file=f)
        #f.write(unicode(text, errors= ignore))


if __name__ == '__main__':
    
    r = 2
    power = int(sys.argv[1])
    N = r**power # roughly 2 billion
    funcs = [_generate_const_seq, _generate_checkerboard_seq, _generate_random_seq, _generate_rudin_shapiro_seq,
    _generate_thue_morse_seq, _generate_fibonacci_seq, _generate_baum_sweet_seq, 
    _generate_dragon_seq, _generate_ehrenfeucht_mycielski_seq]
    ''', _generate_kolakoski_seq, generate_pi_seq'''
    
    for i in funcs:
        N = r**power
        if(i == _generate_ehrenfeucht_mycielski_seq):
            if(power>19):
                N = r**19

        print(str(i.__name__))
        a = i(N)
        #print(a)
        s= ""
        for l in range(len(a)):
            s+=str(a[l])
        #print(s)
        print(type(s))
        #string_for_output = s.encode('utf8', 'replace')
        printOut(str("/Users/Roy/Research/Chaikin/InformationTheory/sequences/sequence"+ i.__name__+"r_"+str(r)+"to"+str(power)+".txt"), s)
        #printOut("/Users/Roy/Research/Chaikin/InformationTheory/sequences/sequence"+ i.__name__+".txt", s)
        print("\n")


    '''
    _generate_const_seq(N)
    #generate_const_seq(N, seq)
    _generate_checkerboard_seq(N)
    #generate_checkerboard_seq(N, seq):
    _generate_random_seq(N):
    #generate_random_seq(N, seq):
    _generate_rudin_shapiro_seq(N, Nstart=0):
    #generate_rudin_shapiro_seq(N, seq):
    _generate_thue_morse_seq(N, Nstart=0)
    #generate_thue_morse_seq(N, seq)
    _generate_fibonacci_seq(N, Nstart=0)
    #generate_fibonacci_seq(N, seq)
    _generate_kolakoski_seq(N)
    #generate_kolakoski_seq(N, seq)
    _generate_baum_sweet_seq(N, Nstart=0):
    #generate_baum_sweet_seq(N, seq)
    _generate_dragon_seq(N, Nstart=0)
    #generate_dragon_seq(N, seq):
    _generate_ehrenfeucht_mycielski_seq(N, Nstart=0) # makes sequence length of N
    #generate_ehrenfeucht_mycielski_seq(N, seq) # appends however much to sequence 'seq' in order to make it length N
    generate_pi_seq(N, Nstart=0) '''












