import time


class TimeSinceProcessStart():
    def __init__(self):
        self.start = time.time()
        self.end = time.time()

    def get(self):
        self.end = time.time()
        elapsed = self.end - self.start
        return int(elapsed)


class BPMTicker():
    def __init__(self, bpm, bpb):
        self.start_bpm = time.time()
        self.start_bpb = time.time()
        self.end = time.time()
        self.bpmDelay = 60 / bpm
        self.bpbDelay = 60 / (bpm / bpb)

    def isTicking(self):
        self.end = time.time()
        is_bpm_ticking = self.end - self.start_bpm >= self.bpmDelay
        is_bpb_ticking = self.end - self.start_bpb >= self.bpbDelay
        if(is_bpb_ticking):
            self.start_bpm = time.time()
            self.start_bpb = time.time()
            return 2
        if(is_bpm_ticking):
            self.start_bpm = time.time()
            return 1
        return 0


if __name__ == "__main__":

    timeSinceProcessStart = TimeSinceProcessStart()
    bpmTicker = BPMTicker(120, 4)
    while True:
        # print(timeSinceProcessStart.get())
        toto = bpmTicker.isTicking()
        if(toto == 1):
            print("toto")
        if(toto == 2):
            print("titi")
