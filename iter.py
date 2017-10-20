#!/ctc/sw/v6/14.12/bin/python

import sys
import random
import pandas
import timeit

def iter_pandas(l, df) :
    df.ix[0, 'Y_EWMA'] = l * df.ix[0, 'A'] + (1-l) * df.ix[0, 'Y']
    for i in range(1, len(df)):
        df.ix[i,'Y_EWMA'] = l * (df.ix[i-1,'Y_EWMA'] + df.ix[i,'A']) + (1-l) * df.ix[i,'Y']

def iter_normal(l, A, Y) :
    B = [l*A[0] + (1-l)*Y[0]]
    for i in range(1,len(A)) :
        B.append(l*(B[i-1] + A[i]) + (1-l)*Y[i])

# Size of input arrays (default 100)
n = 100 if len(sys.argv) == 1 else int(sys.argv[1])

# Set up input arrays
random.seed()
l = random.randint(0, 1000)/1000.0
A = [random.randint(0, 1000)/1000.0 for i in range(n)]
Y = [random.randint(0, 1000)/1000.0 for i in range(n)]
df = pandas.DataFrame({'A':A, 'Y':Y, 'Y_EWMA':n*[0]})

# Time our two functions
runs = 10
print 'len(A) == len(Y) == len(Y_EWMA) == %d' % n
print 'normal: %.6fs' % (timeit.timeit(lambda: iter_normal(l,A,Y), number=runs)/runs)
print 'pandas: %.6fs' % (timeit.timeit(lambda: iter_pandas(l,df), number=runs)/runs)
