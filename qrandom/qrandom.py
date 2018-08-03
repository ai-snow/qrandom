from collections import deque


class QRandom(object):

    def __init__(self, random):
        self.random = random
        self.quantiles = {}
        self.buffer = []
        self.buffer_index = 0

    def __quantile(self):
        pass

    def __getattribute__(self, attr):
        if attr.startswith('q_'):
            quantile_name = attr[2:]
            quantile = self.random.random()
            self.buffer.append(quantile)
            if quantile_name not in self.quantiles:
                self.quantiles[quantile_name] = deque()
            self.quantiles[quantile_name].appendleft(self.buffer_index)
            self.buffer_index += 1
            return quantile
        else:
            return super(QRandom, self).__getattribute__(attr)