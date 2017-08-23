


from datetime import datetime


def saveAFileAppend(tnimi, contents):
    fo = open(tnimi  , "a")
    fo.write( contents);
    # Close opend file
    fo.close()



def logtime(logfil,action, indx):
    nowtime= datetime.now()
    loglinestr = action + "; " + str(indx) + "; " + str(nowtime)
    saveAFileAppend(logfil, loglinestr + "\n")

    print (loglinestr)