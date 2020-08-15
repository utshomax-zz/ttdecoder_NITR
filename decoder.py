
import sqlite3

#extras
pslot=['PB','PD','PE','PF','PG','PH','PY','PX']
slotList=['TA','TB','TC','TD','TE','TF','TG','TJ','TK','TL','TM','PA','PB','PD','PE','PF','PG','PH','PY','PX']
seq={'CS':'PT'}
tkey={'M1':'8.00-8.55','M2':'9.00-9.55','M3':'10.00-10.55','M4':'11.05-12.00','A5':'1.15-2.10','A6':'2.15-3.10','A7':'3.20-4.15','A8':'4.20-5.15'}

#get specific sequence for branch
def loaddb(quiry,pram):
   
    try:
        conn = sqlite3.connect('routine.db')#pylint: disable=E1101
        cursor = conn.cursor()
        res= conn.execute(quiry,pram)
        num=res.fetchall()
        conn.commit()
        cursor.close()
        return num
        

    except sqlite3.Error as error:#pylint: disable=E1101
        #send a notifiacation to me!
        print("db error!",error)
    finally:
        if (conn):
            conn.close()

#add to db
def addTodb(quiry):
   
    try:
        conn = sqlite3.connect('idroutine.db')#pylint: disable=E1101
        cursor = conn.cursor()
        conn.execute(quiry)
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:#pylint: disable=E1101
        #send a notifiacation to me!
        print("db error!",error)
    finally:
        if (conn):
            conn.close()        

def getBranch(roll):
    b=roll[3:5]
    print(b)
    return b

def simplify(timeinfo):
    p=None
    stime=[]
    for day in timeinfo:
        if len(timeinfo[day])>1:
            t=timeinfo[day][0]
            s=t[1]
            p='P{}'.format(s)
        else:
            p=timeinfo[day][0] 
        t=(day,p)
        stime.append(t)
    return stime
       # for time in timeinfo[day]:

            

#saving customized routine
def saveTodb(subject,time,uid):
    for singleSlot in time:
        qui='''INSERT INTO idroutine (userid ,sub ,day,time) VALUES(?,?,?,?)'''
        pramitar=(uid,subejct,singleSlot[0],singleSlot[1])
        loaddb(qui,pramitar)
        print(singleSlot,subejct,uid)



#main algorithom
def getTime(subject,slot,roll,uid):
    slot=slot.upper()
    print(slot)
    if slot in slotList:
        branch=getBranch(roll)
        ftime={}
        itime=[]
        p=(slot,)
        for time in tkey.keys():
            if slot not in pslot:
                itime=[]
            q='''SELECT * FROM routine WHERE {} = ?'''.format(time)
            result=loaddb(q,p)
            if result: 
                if time not in itime:
                    itime.append(time)                       
                for i in result:
                    if i[0] not in ftime:
                        ftime[i[0]]=itime
        stime=simplify(ftime)
        saveTodb(subejct,stime,uid)


   # return ftime



#geting the slot input and branch

print('First Subjet')

subejct,slot,roll,uid=input().split()
getTime(subejct,slot,roll,uid)