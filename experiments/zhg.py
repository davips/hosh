"""
Example of identifiers from diferent subgroups in G.
"""

from hosh import Hosh

z = 2 ** 32
h = z * 2 ** 96
g = h * 2 ** 64
lasthex = b64dec("ffffffffffffffffffffffffffffffff")
p = 2 ** 32 - 5

# rho = "--------------------------------"
# lastd = "----------------ZZZZZZZZZZZZZZZZ"
# d = "-------------------------------0"
# print(f"last in Z = {b64enc(p - 1, digits=32)} :\t  2^{log(p - 1, 2):.12f}", p - 1)
# print(f"last in H = {b64enc(p ** 4 - 1, digits=32)} :\t 2^{log(p ** 4 - 1, 2):.12f}", p ** 4 - 1)
# print(f"lasthex   = {b64enc(lasthex, digits=32)} :\t 2^{log(lasthex, 2):.12f}", lasthex)
# print(f"last del  = {lastd} :\t 2^{log(b64dec(lastd), 2):.12f}", b64dec(lastd))
# print(f"first del = {d} :\t 2^{log(b64dec(d), 2):.12f}", b64dec(d))
# print(f"rho       = {rho} :\t 2^{log(b64dec(rho), 2):.12f}", b64dec(rho))
# print(f"last in G = {b64enc(p ** 6 - 1, digits=32)} :\t 2^{log(p ** 6 - 1, 2):.12f}", p ** 6 - 1)
#
# # for i in range(1000000):
# #     if isprime(p**6 - i):
# #         break
# # print(i)
# import numpy as np
#
# a = np.array([
#     [1, 0, 7, 8],
#     [0, 1, 5, 9],
#     [0, 0, 1, 0],
#     [0, 0, 0, 1]
# ])
# b = np.array([
#     [1, 0, 6, 3],
#     [0, 1, 5, 7],
#     [0, 0, 1, 9],
#     [0, 0, 0, 1]
# ])
# print(a @ b)
# print((a @ b % 11).data == (b @ a % 11).data)
# print()
# print()

l = Hosh.fromn(4 * p // 5, p, p ** 6)
x = Hosh.fromn(3 * p ** 4 // 5, p, p ** 6)
y = Hosh.fromn(4 * p ** 4 // 5, p, p ** 6)
f = Hosh.fromn(3 * p ** 6 // 5, p, p ** 6)
g = Hosh.fromn(4 * p ** 6 // 5, p, p ** 6)
print(l.cells)
print(x.cells, y.cells)
print(f.cells, g.cells)
print("l * f == f * l", l * f == f * l)
print("x * y == y * x", x * y == y * x)
print("f * x != x * f", f * x != x * f)
print()
print("l * f * g * x * y == f * l * g * y * x == f * g * l * y * x == f * g * y * l * x == f * g * y * x * l",
      l * f * g * x * y == f * l * g * y * x == f * g * l * y * x == f * g * y * l * x == f * g * y * x * l)

print(f * x * y * ~x == f * y)

a = Hosh.fromn(4 * p // 5, p, p ** 6)
print(a, ~a)

a = Hosh.fromn(4 * p ** 4 // 5, p, p ** 6)
print(a, (~a))


print()
print(x*f)
print(f*x)
