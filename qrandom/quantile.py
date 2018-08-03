from collections import deque


class Quantile(object):
    
    def parse(input):
        values = input.split('\t')
        quantile = Quantile(values[0])
        for val in values[1:]:
            quantile.waiting.appendleft(int(val))
        return quantile
    
    def __init__(self, name):
        self.name = name
        self.used = deque()
        self.waiting = deque()
        
    def prime(self):
        self.waiting = self.used
        self.used = deque()
        
    def serialize(self):
        values = [self.name]
        self.used.reverse()
        for value in [str(q) for q in self.used]:
            values.append(value)
        self.used.reverse()
        return '\t'.join(values)