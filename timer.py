from datetime import datetime

class Timer():

    def __init__(self):
        self.START = None
        self.END = None
        self._total = 0
        self.step = 0

    def start(self):
        self.START = datetime.now()
        print(self.START)

    def end(self):
        self.END = datetime.now()
        print(self.END)

    def s2d(self, seconds):
        SECOND = int(seconds % 60)
        MINUTE = int((seconds//60) % 60)
        HOUR = int((seconds//3600) % 24)
        DAY = int((seconds//86400))
        return DAY, HOUR, MINUTE, SECOND

    def printlog(self):
        """
        use start()
        use end()
        use printlog()
        """
        DURATION = self.END - self.START
        print(self.END)
        s = DURATION.total_seconds()
        DAY, HOUR, MINUTE, SECOND = self.s2d(s)
        print('it takes you {}:{}:{}\':{}" to run this script.'.format(DAY, HOUR, MINUTE, SECOND))

    def tick(self, length=1):
        self.step += length

    def loading(self):
        """
        set `_total`
        use start()
        use tick()
        use loading()
        """
        percent = self.step*100/self._total
        now = datetime.now()
        passed = now - self.START
        passed = int(passed.total_seconds())
        if percent != 0:
            remaining = (passed*100//percent) - passed
            DAY, HOUR, MINUTE, SECOND = self.s2d(remaining)
        else:
            DAY, HOUR, MINUTE, SECOND = '-', '-', '-', '-'
        ETA = '{}:{}:{}:{}'.format(DAY, HOUR, MINUTE, SECOND)
        DAY1, HOUR, MINUTE, SECOND = self.s2d(passed)
        ET = '{}:{}:{}:{}'.format(DAY1, HOUR, MINUTE, SECOND)
        print('\r {}'.format(' '*120), end='\r')
        print('\r{:,} of {:,} | {:.4f}% \tET:{} \tETA:{} {}'.format(self.step, self._total, percent, ET, ETA, ' '*10), end='\r')
