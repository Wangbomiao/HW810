from collections import defaultdict
from prettytable import PrettyTable
from Fileread import filereader
import os
import unittest
import sqlite3


class Repositor:

    def __init__(self,paths):
        self.paths=paths
        self.st=dict()
        self.ins=dict()
        
    def student(self,path):
        stpath=os.path.join(self.paths,path)

        for cwid,name,major in filereader(stpath,3,sep='\t',header=False):
            if cwid in self.st:
                raise Exception('Warning : cwid {} already read from the file'.format(cwid))
            else:
                self.st[cwid]=Student(cwid,name,major)

    def instuctor(self,path):
        inspath=os.path.join(self.paths,path)
       
        for cwid,name,dept in filereader(inspath,3,sep='\t',header=False):
            if cwid in self.ins:
                raise Exception('Warning : cwid {} already read from the file'.format(cwid))
            else:
                self.ins[cwid]=Instuctor(cwid,name,dept)

    def grade(self,path):
        gradepath=os.path.join(self.paths,path)

        for stcwid,course,grade,inscwid in filereader(gradepath,4,sep='\t',header=False):

            if stcwid in self.st:
                self.st[stcwid].add_course(course,grade)
            else:
                raise Exception('Warning : student cwid {} already read from the file'.format(stcwid))

            if inscwid in self.ins:
                self.ins[inscwid].add_coursenum(course)
            else:
                raise Exception('Warning : instuctor cwid {} already read from the file'.format(inscwid))
    
    def stpt(self):
        stpt=PrettyTable(field_names=['cwid','name','completed course'])

        for key in self.st:
            stpt.add_row([key,self.st[key].name,list(self.st[key].cour.items())])
        print(stpt)
    
    def inspt(self):
        inspt=PrettyTable(field_names=['cwid','name','dept','course','student'])
        db=sqlite3.connect('C:\sqlite\homework11.db')
        for row in db.execute('select HW11_instructors.CWID,HW11_instructors.Name,HW11_instructors.Dept,HW11_grades.Course,COUNT(HW11_grades.Course)\
                              from HW11_grades join HW11_instructors on HW11_grades.Instructor_CWID=HW11_instructors.CWID\
                              GROUP BY HW11_instructors.CWID,HW11_instructors.Name,HW11_instructors.Dept,HW11_grades.Course'):
                row1=list(row)
                inspt.add_row(row1)
        print(inspt)


class Student:

    def __init__(self,cwid,name,major):
        self.cwid=cwid
        self.name=name
        self.major=major
        self.cour=dict()

    def add_course(self,course,grade):
        self.cour[course]=grade

    def stptstring(self):
        return [self.cwid,self.name,self.major,sorted(self.cour.items())]
    

class Instuctor:
    
    def __init__(self,cwid,name,dept):
        self.cwid=cwid
        self.name=name
        self.dept=dept
        self.cournum=defaultdict(int)

    def add_coursenum(self,course):
        self.cournum[course]+=1

    def insstring(self):
        for course,student in self.cournum.items():
            yield [self.cwid,self.name,self.dept,course,student]


class RepositorTest(unittest.TestCase):
    def testrepositor(self):
        stevens=Repositor(r'C:\Users\wangd\学习和作业需要\810\week9资料')
        stevens.student('students.txt')
        stevens.instuctor('instructors.txt')
        stevens.grade('grades.txt')
        stevens.inspt()
        stevens.stpt()
        student_details=[s.stptstring() for s in stevens.st.values()]
        instucroe_details=[i.insstring(course,student) for i in stevens.ins.values() for course,student in i.cournum.items() ]
        students=[['10103', 'Baldwin, C', 'SFEN', [('CS 501', 'B'), ('SSW 564', 'A-'), ('SSW 567', 'A'), ('SSW 687', 'B')]],\
                  ['10115', 'Wyatt, X', 'SFEN', [('CS 545', 'A'), ('SSW 564', 'B+'), ('SSW 567', 'A'), ('SSW 687', 'A')]], \
                  ['10172', 'Forbes, I', 'SFEN', [('SSW 555', 'A'), ('SSW 567', 'A-')]],\
                  ['10175', 'Erickson, D', 'SFEN', [('SSW 564', 'A'), ('SSW 567', 'A'), ('SSW 687', 'B-')]],\
                  ['10183', 'Chapman, O', 'SFEN', [('SSW 689', 'A')]],\
                  ['11399', 'Cordova, I', 'SYEN', [('SSW 540', 'B')]],\
                  ['11461', 'Wright, U', 'SYEN', [('SYS 611', 'A'), ('SYS 750', 'A-'), ('SYS 800', 'A')]],\
                  ['11658', 'Kelly, P', 'SYEN', [('SSW 540', 'F')]],\
                  ['11714', 'Morton, A', 'SYEN', [('SYS 611', 'A'), ('SYS 645', 'C')]],\
                  ['11788', 'Fuller, E', 'SYEN', [('SSW 540', 'A')]]]
        instuctor=[['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4],\
                  ['98765', 'Einstein, A', 'SFEN', 'SSW 540', 3], \
                  ['98764', 'Feynman, R', 'SFEN', 'SSW 564', 3],\
                  ['98764', 'Feynman, R', 'SFEN', 'SSW 687', 3],\
                  ['98764', 'Feynman, R', 'SFEN', 'CS 501', 1],\
                  ['98764', 'Feynman, R', 'SFEN', 'CS 545', 1],\
                  ['98763', 'Newton, I', 'SFEN', 'SSW 555', 1],\
                  ['98763', 'Newton, I', 'SFEN', 'SSW 689', 1],\
                  ['98760', 'Darwin, C', 'SYEN', 'SYS 800', 1],\
                  ['98760', 'Darwin, C', 'SYEN', 'SYS 750', 1],\
                  ['98760', 'Darwin, C', 'SYEN', 'SYS 611', 2],\
                  ['98760', 'Darwin, C', 'SYEN', 'SYS 645', 1]]
        self.assertEqual(student_details,students)
        self.assertEqual(instucroe_details,instuctor)


if __name__ == '__main__':
    # note: there is no main(). Only test cases here
    unittest.main(exit=False, verbosity=2)

