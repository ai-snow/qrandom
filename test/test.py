from random import Random

from qrandom.qrandom import QRandom

q = QRandom(Random())

first = q.q_first
second = q.q_second
first = q.q_first

print(q.quantiles)
print(q.buffer)
