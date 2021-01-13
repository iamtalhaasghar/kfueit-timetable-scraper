
CLASSES_FOLDER = 'classes'
TIME_TABLE_LINK = 'https://my.kfueit.edu.pk/users/testtable'
SEMESTER_LINK = '''https://my.kfueit.edu.pk/users/testtable?filter=class&timetablename=KFUEIT+Spring+2019+Timetable+1.0%28w.e.f.+10+June+2019%29&department=&sets=<semester>&teacher=&room='''
SEMESTER_KEYWORD = '<semester>'
ROOM_LINK = '''https://my.kfueit.edu.pk/users/testtable?filter=room&timetablename=KFUEIT+Spring+2019+Timetable+1.0%28w.e.f.+10+June+2019%29&department=&sets=&teacher=&room=<room>'''
ROOM_KEYWORD = '<room>'
ROOM_FOLDER = 'rooms'
TEACHER_LINK = '''https://my.kfueit.edu.pk/users/testtable?filter=teacher&timetablename=KFUEIT+Spring+2019+Timetable+1.0%28w.e.f.+10+June+2019%29&department=&sets=&teacher=<teacher>&room='''
TEACHER_KEYWORD = '<teacher>'
TEACHER_FOLDER = 'teachers'

def fetchListOf(identifier):
    from urllib.request import urlopen
    data = urlopen(TIME_TABLE_LINK)
    from bs4 import BeautifulSoup as bs
    data = bs(data.read(),'html.parser')
    theList = list()
    for c in data.find(id=identifier):
        temp = c.string
        if(temp != None and len(temp.strip())!=0 and temp!='None'):
            theList.append('%s' % temp.strip())

    return theList

def fetchPrintableArea(link, keyword, item):
    from urllib.request import urlopen
    from bs4 import BeautifulSoup as bs
    link = link.replace(keyword, item)
    data = urlopen(link)
    t = bs(data.read() ,'html.parser')
    t = t.find(id='printableArea')
    return str(t)
    
def autoFetchClasswiseTimeTable():
    classesList = fetchListOf('class')
    for i in classesList:
        print('Fetching timetable of : %s' % i)
        temp = fetchPrintableArea(SEMESTER_LINK, SEMESTER_KEYWORD, i)
        import os
        if(not os.path.exists('%s/%s' %(os.getcwd(), CLASSES_FOLDER))):
            os.mkdir(CLASSES_FOLDER)
        f = open('%s/%s.txt' %(CLASSES_FOLDER,i),'w')
        f.write(temp)
        f.close()

def autoFetchRoomwiseTimeTable():
    roomsList = fetchListOf('room')
    for i in roomsList:
        print('Fetching timetable of : %s' % i)
        temp = fetchPrintableArea(ROOM_LINK, ROOM_KEYWORD, i.replace(' ','+'))
        import os
        if(not os.path.exists('%s/%s' %(os.getcwd(), ROOM_FOLDER))):
            os.mkdir(ROOM_FOLDER)
        f = open('%s/%s.txt' %(ROOM_FOLDER,i),'w')
        f.write(temp)
        f.close()
def autoFetchTeacherwiseTimeTable():
    roomsList = fetchListOf('teacher')
    for i in roomsList:
        print('Fetching timetable of : %s' % i)
        temp = fetchPrintableArea(TEACHER_LINK, TEACHER_KEYWORD, i.replace(' ','+'))
        import os
        if(not os.path.exists('%s/%s' %(os.getcwd(), TEACHER_FOLDER))):
            os.mkdir(TEACHER_FOLDER)
        f = open('%s/%s.txt' %(TEACHER_FOLDER,i),'w')
        f.write(temp)
        f.close()
if __name__ == "__main__":
    autoFetchClasswiseTimeTable()
    autoFetchRoomwiseTimeTable()
    autoFetchTeacherwiseTimeTable()
