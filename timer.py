from datetime import datetime

START = None
END = None

def start():
    global START
    START = datetime.utcnow()
    print(START)

def end():
    global END
    END = datetime.utcnow()
    print(END)

def s2d(seconds):
    SECOND = int(seconds % 60)
    MINUTE = int((seconds//60) % 60)
    HOUR = int((seconds//3600) % 24)
    DAY = int((seconds//86400))
    return DAY, HOUR, MINUTE, SECOND

def printlog():
    """
    use start()
    use end()
    use printlog()
    """
    DURATION = END - START
    print(END)
    s = DURATION.seconds
    DAY, HOUR, MINUTE, SECOND = s2d(s)
    print('it takes you {}:{}:{}\':{}" to run this script.'.format(DAY, HOUR, MINUTE, SECOND))

_total = 0
step = 0
def tick():
    global step
    step += 1

def loading():
    """
    set `_total`
    use start()
    use tick()
    use loading()
    """
    percent = step*100/_total
    now = datetime.utcnow()
    passed = now - START
    passed = passed.seconds
    remaining = (passed*100//percent) - passed
    DAY, HOUR, MINUTE, SECOND = s2d(remaining)
    ETA = '{}:{}:{}:{}'.format(DAY, HOUR, MINUTE, SECOND)
    DAY, HOUR, MINUTE, SECOND = s2d(passed)
    ET = '{}:{}:{}:{}'.format(DAY, HOUR, MINUTE, SECOND)
    print('\r {}'.format(' '*120), end='\r')
    print('\r{} of {} | {}% \tET:{} \tETA:{} {}'.format(step, _total, percent, ET, ETA, ' '*10), end='\r')
