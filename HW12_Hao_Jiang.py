#coding=utf-8
#author:Hao Jiang
#homework12
from typing import Tuple, Iterator,List
import unittest
import os,prettytable
from prettytable import PrettyTable
from collections import defaultdict
import sqlite3

def file_reader(path, fields, sep=',', header=False) -> Iterator[Tuple[str]]: #open the file
    try:
        fp = open(path,'r')
    except FileNotFoundError as e:  #if enter the file name not exit will get a warning
        print(e)
    else:
        while True:
            a=fp.readline()
            if header is True:
                header=False
                continue
            if a=='':
                break
            a=a.split(sep)
            if a[fields-1][-1]=='\n':
                a[fields-1]=a[fields-1][:-1]
            if len(a)!= fields:
                raise ValueError    
            yield a


class Student: #record students information
    def __init__(self , s_cwid , s_name , s_majior):
        self.s_cwid = s_cwid
        self.s_name = s_name
        self.s_major = s_majior
        self.s_course_grade =dict()
        self.s_completed_course=list()
        self.s_require_course=dict()
        self.gpa=0
    
    def get_coursegrade(self , course , grade):
        self.s_course_grade[course] = grade

    def get_require_course(self,course,require):
            self.s_require_course[course]=require
    
    def get_gpa(self): #caculate average gpa
        grade_val = {'A':4.0,'A-':3.75,'B+':3.25,'B':3.0,'B-':2.75,'C+':2.25,'C':2.0,'C-':0,'D+':0,'D':0,'D-':0,'F':0}
        grade_sum=0
        for j,i in self.s_course_grade.items():
            if grade_val[i]>=0:
                grade_sum+=grade_val[i]
                self.s_completed_course.append(j)
                if j in self.s_require_course.keys():
                    del self.s_require_course[j]
        num_course=len(self.s_course_grade)
        if num_course>0:
            self.gpa=grade_sum/num_course
    def get_require(self):
        a=list()
        for i, j in self.s_require_course.items():
            if j=='R':
                a.append(i)
        return a
    def get_election(self):
        a=list()
        for i, j in self.s_require_course.items():
            if j=='E':
                a.append(i)
        return a

class Instructor: #record teacher information
    def __init__(self , i_cwid , i_name , i_department):
        self.i_cwid = i_cwid
        self.i_name = i_name
        self.i_department = i_department
        self.i_studentnum = defaultdict(int)

    def count_studentsnum(self,course): #the student num
        self.i_studentnum[course] += 1


class FileAnalyzer:
    def __init__(self, directory: str) -> None:
        self.directory: str = directory
        self.studentdict = dict()
        self.instructordict = dict()
        self.major=defaultdict(lambda: defaultdict(str))
        self.student(os.path.join(directory,'students.txt'))
        self.instructor(os.path.join(directory,'instructors.txt'))
        self.majors(os.path.join(directory,'majors.txt'))
        self.gradesget(os.path.join(directory,'grades.txt'))

    def student(self,path): #open file and create a dictionary
        for i in file_reader(path,3,'\t',True):
            s_cwid , s_name , s_major = i[0],i[1],i[2]
            self.studentdict[s_cwid] = Student(s_cwid , s_name , s_major)

    def instructor(self,path): #open file and create a dictionary
        for i in file_reader(path,3,'\t',True):
            i_cwid , i_name , i_department = i[0],i[1],i[2]
            self.instructordict[i_cwid] = Instructor(i_cwid , i_name , i_department)

    def majors(self,path:str):  #elective and required courses are carried out according to the majors
        for i in file_reader(path,3,'\t',True):
            majors , reqire , course = i[0],i[1],i[2]
            self.major[majors][course] = reqire
            for x in self.studentdict.keys():
                if majors==self.studentdict[x].s_major:
                    self.studentdict[x].get_require_course(course,reqire)
               

    def gradesget(self,path) : #open file and create a dictionary
        for i in file_reader(path,4,'\t',True):
            s_cwid , s_course , g_grade , i_cwid = i[0],i[1],i[2],i[3]
            if s_cwid in self.studentdict.keys():
                self.studentdict[s_cwid].get_coursegrade(s_course,g_grade)                
            if i_cwid in self.instructordict.keys():
                self.instructordict[i_cwid].count_studentsnum(s_course)
        for x in self.studentdict.keys():
            self.studentdict[x].get_gpa()

    def pretty_print(self) -> None: #Print all students and instructors prettytable
        pt : PrettyTable = PrettyTable(field_names=["CWID","NAME","Completed Course",'require course','Elect course','gpa'])
        for i in  self.studentdict.values():
            requiress=sorted(list(i.get_require()))
            elecitonss=sorted(list(i.get_election()))
            pt.add_row([i.s_cwid,i.s_name,sorted(i.s_completed_course),requiress,elecitonss,round(i.gpa,2)])
        print (pt)
        tb : PrettyTable = PrettyTable(field_names=["CWID","NAME","Dept","Course","Students"])
        for p in  self.instructordict.values():
            for x,y in p.i_studentnum.items():
                tb.add_row([p.i_cwid,p.i_name,p.i_department,x,y])
        print (tb)
        mb : PrettyTable = PrettyTable(field_names=["Major",'require course','Elect course'])

        for i in  self.major.keys():
            requiress=list()
            elecitonss=list()
            j=self.major[i]
            for x in j.keys():
                if self.major[i][x]=='R':
                    requiress.append(x)
                else:
                    elecitonss.append(x)
            mb.add_row([i,requiress,elecitonss])
        print (mb)

        
        sss = sqlite3.connect('HW11(1).db')
        cccc = sss.cursor()

        aaa = cccc.execute("select e.Name , e.CWID , e.Course , e.Grade,instructors.Name from (students inner join grades on grades.StudentCWID==students.CWID)     as e     inner join instructors on e.InstructorCWID==instructors.CWID")
        
        mmp : PrettyTable = PrettyTable(field_names=["NAME","CWID","Course","Grade","instructor"])
        for x in aaa:
             mmp.add_row(x)
        print(mmp)
         
def main():
    directory=os.getcwd()
    repo = FileAnalyzer(directory)
    repo.pretty_print()

if __name__ == '__main__':
    main()