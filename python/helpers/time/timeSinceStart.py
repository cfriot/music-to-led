import time

class TimeSinceStart():
    def __init__(self):
        self.start = time.time()
        self.end = time.time()

    def restart(self):
        self.start = time.time()

    def get(self):
        self.end = time.time()
        elapsed = self.end - self.start
        return int(elapsed)

    def getMs(self):
        self.end = time.time()
        elapsed = self.end - self.start
        elapsed *= 100
        return int(elapsed)

if __name__ == "__main__":

    print('Starting timeSinceStart test on ports :')

    timeSinceStart = TimeSinceStart()
    while True:
        print(timeSinceStart.getMs())
