from qrandom.quantile import Quantile


class QRandom(object):

    def restore(filename, random):
        with open(filename, 'r') as f:
            line_ct = 0
            for line in f:
                line_ct += 1
                if line_ct == 1:
                    qr = QRandom(random, int(line))
                elif line_ct == 2:
                    qr.__fill_buffer(int(line))
                else:
                    if line:
                        q = Quantile.parse(line)
                        qr.quantiles[q.name] = q
        
        return qr
    
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
            return self.q(quantile_name)
        else:
            return super(QRandom, self).__getattribute__(attr)
    
    def q(self, quantile_name):
        if quantile_name not in self.quantiles:
                self.quantiles[quantile_name] = Quantile(quantile_name)
        quantile = self.quantiles[quantile_name]

        if len(quantile.waiting):
            index = quantile.waiting.pop()
        else:
            index = len(self.buffer)
        
        q = self.__fill_buffer(index)
        quantile.used.appendleft(index)

        return q

    def reset(self):
        for _, quantile in self.quantiles.items():
            quantile.prime()

    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self.seed) + '\n')
            f.write(str(len(self.buffer)) + '\n')
            for _, q in self.quantiles.items():
                f.write(q.serialize() + '\n')