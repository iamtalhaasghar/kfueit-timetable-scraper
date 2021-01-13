from flask import Flask
from flask import render_template
from flask import escape
from flask import Markup
from flask import redirect
from scrapper import *

app = Flask(__name__)
tempList = list()

@app.route('/')
def showHomePage():
    return render_template('index.html')

@app.route('/list/<listOf>')
def showListPage(listOf):
    import os
    if(listOf == 'class'):
        p = os.listdir(CLASSES_FOLDER)
    elif(listOf == 'teacher'):
        p = os.listdir(TEACHER_FOLDER)
    elif(listOf == 'room'):
        p = os.listdir(ROOM_FOLDER)
    htmlResponse = str()
    for i in p:
        i = i.split('.txt')[0]
        htmlResponse += '<p>%s</p><br>'%(i)
    return htmlResponse

@app.route('/download/<fileFormat>/<category>/<fileName>')
def showTimeTable(fileFormat,category,fileName):
    if (fileName == 'start'):
        import os
        if(category == 'class'):
            p = os.listdir(CLASSES_FOLDER)
        elif(category == 'teacher'):
            p = os.listdir(TEACHER_FOLDER)
        elif(category == 'room'):
            p = os.listdir(ROOM_FOLDER)
        for i in p:
            i = i.split('.txt')[0]
            tempList.append('/download/%s/%s/%s' %(fileFormat,category,i))
        return redirect(tempList.pop())

    elif(fileName == 'complete'):
        return '<h1>Download Complete!!!</h1>'
    
    if(category == 'class'):
            p = open('%s/%s.txt'%(CLASSES_FOLDER,fileName)).read()
    elif(category == 'teacher'):
            p = open('%s/%s.txt'%(TEACHER_FOLDER,fileName)).read()
    elif(category == 'room'):
            p = open('%s/%s.txt'%(ROOM_FOLDER,fileName)).read()

    h = open('templates/source.html').read()
    if(fileFormat == 'pdf'):
        h = h.replace('{{function_to_call}}','exportPDF()')
    else:
        h = h.replace('{{function_to_call}}','exportToExcel()')
    h = h.replace('{{to_print}}', p)
    h = h.replace('{{current_file_name}}', fileName)

    if(len(tempList) == 0):
        h = h.replace('{{next_file_link}}', ('/download/%s/%s/%s' %(fileFormat,category,'complete')))
    else:
        h = h.replace('{{next_file_link}}', tempList.pop())
    return (h)

if __name__=='__main__':
    app.run(debug=True)
