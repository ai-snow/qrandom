from collections import deque


from quantile import Quantile


class QRandom(object):

    def __init__(self, random, seed):
        self.random = random
        self.seed = seed
        self.random.seed(seed)
        self.quantiles = {}
        self.buffer = []

    def __fill_buffer(self, index):
        while len(self.buffer) <= index:
            self.buffer.append(self.random.random())
            
        return self.buffer[index]
        
    def __getattribute__(self, attr):
        if attr.startswith('q_'):
            quantile_name = attr[2:]
            if quantile_name not in self.quantiles:
                self.quantiles[quantile_name] = Quantile()
            quantile = self.quantiles[quantile_name]
            q = None
            if len(quantile.waiting):
                index = quantile.waiting.pop()
                q = self.__fill_buffer(index)
                quantile.used.appendleft(index)
            else:
                index = len(self.buffer)
                q = self.__fill_buffer(index)
                quantile.used.appendleft(index)
                
            return q
        else:
            return super(QRandom, self).__getattribute__(attr)
    
    def reset(self):
        self.random.seed(self.seed)
        
        for _, quantile in self.quantiles:
            quantile.prime()
