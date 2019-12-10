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
    DAY = (s//3600)//24
    HOUR = (s//3600) - (DAY*24)
    MINUTE = (s//60) - (HOUR*60) - (DAY*24*60)
    SECOND = s - (MINUTE*60 + HOUR*3600 + DAY*24*3600)
    print('it takes you {}:{}:{}\':{}" to run this script.'.format(DAY, HOUR, MINUTE, SECOND))
