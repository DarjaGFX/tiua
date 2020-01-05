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

def printlog():
    DURATION = END - START
    print(END)
    s = DURATION.seconds
    SECOND = s % 60
    MINUTE = (s//60) % 60
    HOUR = (s//3600) % 24
    DAY = (s//86400)
    print('it takes you {}:{}:{}\':{}" to run this script.'.format(DAY, HOUR, MINUTE, SECOND))
