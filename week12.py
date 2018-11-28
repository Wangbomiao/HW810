import sqlite3
from flask import Flask,render_template
app= Flask(__name__)

@app.route('/instructor_course')

def instructor_course():
    dbfile='C:\sqlite\homework11.db'
    db=sqlite3.connect(dbfile)
    result=db.execute('select HW11_instructors.CWID,HW11_instructors.Name,HW11_instructors.Dept,HW11_grades.Course,COUNT(HW11_grades.Course)\
                              from HW11_grades join HW11_instructors on HW11_grades.Instructor_CWID=HW11_instructors.CWID\
                              GROUP BY HW11_instructors.CWID,HW11_instructors.Name,HW11_instructors.Dept,HW11_grades.Course')
    data=[{'cwid':cwid,'name':name,'dept':dept,'course':course,'student':student} for cwid,name,dept,course,student in result]
    db.close()

    return render_template('instructor_course.html',
                            tltle="Stevens Repository",
                            table_title="Number of students by course and instructor",
                            instructors=data
                            )

app.run(debug=True)