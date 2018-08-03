from random import Random

from qrandom.qrandom import QRandom

q = QRandom(Random(), 1)

print('First run...')
print(q.q_first)
print(q.q_first)

q.reset()

print('Second run...')
print(q.q_first)
print(q.q_second)
print(q.q_first)

print('Stats...')
print(q.quantiles)
print(q.buffer)
