from collections import defaultdict
from prettytable import PrettyTable
from Fileread import filereader
import os
import unittest


class Repositor:

    def __init__(self,paths):
        self.paths=paths
        self.st=dict()
        self.ins=dict()
        self.maj=dict()
        self.re=defaultdict(set)
        self.ele=defaultdict(set)
    def student(self):
        stpath=os.path.join(self.paths,'students.txt')

        for cwid,name,major in filereader(stpath,3,sep='\t',header=False):
            if cwid in self.st:
                raise Exception('Warning : cwid {} already read from the file'.format(cwid))
            else:
                self.st[cwid]=Student(cwid,name,major)

    def instuctor(self):
        inspath=os.path.join(self.paths,'instructors.txt')

        for cwid,name,dept in filereader(inspath,3,sep='\t',header=False):
            if cwid in self.ins:
                raise Exception('Warning : cwid {} already read from the file'.format(cwid))
            else:
                self.ins[cwid]=Instuctor(cwid,name,dept)

    def grade(self):
        gradepath=os.path.join(self.paths,'grades.txt')

        for stcwid,course,grade,inscwid in filereader(gradepath,4,sep='\t',header=False):
            
            if stcwid in self.st:
                self.st[stcwid].add_course(course,grade)

                if course in self.maj[self.st[stcwid].major].required:
                
                    if grade in ['A','A-','B','B-','C+','C']:
                        self.re[stcwid].add(course)

                elif course in self.maj[self.st[stcwid].major].electives:

                    if grade in ['A','A-','B','B-','C+','C']:
                        self.ele[stcwid].add(course)

            else:
                raise Exception('Warning : student cwid {} already read from the file'.format(stcwid))


            if inscwid in self.ins:
                self.ins[inscwid].add_coursenum(course)

            else:
                raise Exception('Warning : instuctor cwid {} already read from the file'.format(inscwid))

    def major(self):
        majpath=os.path.join(self.paths,'majors.txt')

        for major,flag,course in filereader(majpath,3,sep="\t",header=False):

            if major not in self.maj:
                self.maj[major]=Major(major)
                self.maj[major].addcourse(flag,course)

            else:
                self.maj[major].addcourse(flag,course)

    def mapt(self):
        mapt=PrettyTable(field_names=['dept','required','electives'])

        for key in self.maj:
            mapt.add_row([key,self.maj[key].required,self.maj[key].electives])

        print(mapt)

    def stpt(self):
        stpt=PrettyTable(field_names=['cwid','name','completed course','remain required','remain electives'])

        for key in self.st:

            self.st[key].re=self.maj[self.st[key].major].required-self.re[key]

            if self.ele[key]==set():
                self.st[key].ele=self.maj[self.st[key].major].electives
            else:
                self.st[key].ele=None

            stpt.add_row([key,self.st[key].name,list(self.st[key].cour.keys()),self.st[key].re,self.st[key].ele])

        print(stpt)
    
    def inspt(self):
        inspt=PrettyTable(field_names=['cwid','name','dept','course','student'])

        for key in self.ins:
            for key1 in self.ins[key].cournum:
                inspt.add_row([key,self.ins[key].name,self.ins[key].dept,key1,self.ins[key].cournum[key1]])

        print(inspt)


class Major:
    def __init__(self,major):
        self.major=major
        self.required=set()
        self.electives=set()
    def addcourse(self,flag,course):
        if flag=='R':
            self.required.add(course)
        elif flag=='E':
            self.electives.add(course)
        else:
            raise ValueError('the flag {flag} is not defined')
    def majstring(self):
        return [self.major,self.required,self.electives]

class Student:

    def __init__(self,cwid,name,major):
        self.cwid=cwid
        self.name=name
        self.major=major
        self.cour=dict()
        self.re=set()
        self.ele=set()

    def add_course(self,course,grade):
        self.cour[course]=grade
   
    def stptstring(self):
        return [self.cwid,self.name,self.major,sorted(self.cour.keys()),self.re,self.ele]
    

class Instuctor:
    
    def __init__(self,cwid,name,dept):
        self.cwid=cwid
        self.name=name
        self.dept=dept
        self.cournum=defaultdict(int)

    def add_coursenum(self,course):
        self.cournum[course]+=1

    def insstring(self,course,student):
        return [self.cwid,self.name,self.dept,course,student]


class RepositorTest(unittest.TestCase):
    def testrepositor(self):
        stevens=Repositor(r'C:\Users\wangd\学习和作业需要\810\week9资料')
        stevens.student()
        stevens.instuctor()
        stevens.major()
        stevens.grade()
        stevens.inspt()
        stevens.stpt()
        stevens.mapt()
        stdetail=[s.stptstring() for s in stevens.st.values()]
        majdetail=[m.majstring() for m in stevens.maj.values()]
        instucroe_details=[i.insstring(course,student) for i in stevens.ins.values() for course,student in i.cournum.items() ]
        student=[['10103', 'Baldwin, C', 'SFEN', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], {'SSW 540', 'SSW 555'}, None],\
         ['10115', 'Wyatt, X', 'SFEN', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], {'SSW 540', 'SSW 564', 'SSW 555'}, None],\
         ['10172', 'Forbes, I', 'SFEN', ['SSW 555', 'SSW 567'], {'SSW 540', 'SSW 564'}, {'CS 513', 'CS 501', 'CS 545'}],\
         ['10175', 'Erickson, D', 'SFEN', ['SSW 564', 'SSW 567', 'SSW 687'], {'SSW 540', 'SSW 555'}, {'CS 513', 'CS 501', 'CS 545'}],\
         ['10183', 'Chapman, O', 'SFEN', ['SSW 689'], {'SSW 567', 'SSW 540', 'SSW 564', 'SSW 555'}, {'CS 513', 'CS 501', 'CS 545'}],\
         ['11399', 'Cordova, I', 'SYEN', ['SSW 540'], {'SYS 612', 'SYS 671', 'SYS 800'}, None], \
         ['11461', 'Wright, U', 'SYEN', ['SYS 611', 'SYS 750', 'SYS 800'], {'SYS 612', 'SYS 671'}, {'SSW 810', 'SSW 540', 'SSW 565'}],\
         ['11658','Kelly, P', 'SYEN', ['SSW 540'], {'SYS 612', 'SYS 671', 'SYS 800'}, {'SSW 810', 'SSW 540', 'SSW 565'}], \
         ['11714', 'Morton, A', 'SYEN', ['SYS 611', 'SYS 645'], {'SYS 612', 'SYS 671', 'SYS 800'}, {'SSW 810', 'SSW 540', 'SSW 565'}],\
         ['11788', 'Fuller, E', 'SYEN', ['SSW 540'], {'SYS 612', 'SYS 671', 'SYS 800'}, None]]
        major=[['SFEN', {'SSW 567', 'SSW 564', 'SSW 540', 'SSW 555'}, {'CS 501', 'CS 513', 'CS 545'}], \
               ['SYEN', {'SYS 671', 'SYS 612', 'SYS 800'}, {'SSW 565', 'SSW 810', 'SSW 540'}]]
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
        self.assertEqual(stdetail,student)
        self.assertEqual(instucroe_details,instuctor)
        self.assertEqual(majdetail,major)


if __name__ == '__main__':
    # note: there is no main(). Only test cases here
    unittest.main(exit=False, verbosity=2)

