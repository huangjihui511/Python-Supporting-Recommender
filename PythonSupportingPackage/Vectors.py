import numpy as np
def vectors(num,dim):
    vectors = []
    for i in range (len(num)):
        a = [0]*dim
        a[num[i]] = 1
        a = np.array(a)
        vectors.append(a)
    return vectors