#!/usr/bin/python3

import numpy as np
print("Q1")
print("\n")
M = np.linspace(2, 26, 25, dtype=int)
print(M)

print("====================")

print("Q2")
print("\n")
M = M.reshape(5,5)
print(M.shape)
print(M)

print("====================")

print("Q3")
print("\n")
M [:, 0] = 0
print(M)

print("====================")

print("Q4")
print("\n")

M = M @ M
print(M)

print("====================")

print("Q5 - 1")
print("\n")


v = M[0, :]
v = np.linalg.norm(v)#sqrt(v.T*v.T)
print(v)

print("====================")
print("\n")
