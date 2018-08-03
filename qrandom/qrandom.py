

class QRandom(object):

    def __init__(self, random):
        self.random = random
        self.buffer = []

    def __quantile(self):
        pass

    def __getattribute__(self, attr):
        print(attr)