from random import Random

from qrandom.qrandom import QRandom

def test_order_preserved():
    q = QRandom(Random(), 1)

    q_first_1_1 = q.q_first
    q_first_1_2 = q.q_first

    q.reset()

    q_first_2_1 = q.q_first
    q_second_2_1 = q.q_second
    q_first_2_2 = q.q_first

    assert q_first_1_1 == q_first_2_1
    assert q_first_1_2 == q_first_2_2
    assert q_second_2_1 != q_first_1_1
    assert q_second_2_1 != q_first_1_2
