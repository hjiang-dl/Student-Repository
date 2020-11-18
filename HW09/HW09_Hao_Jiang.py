#coding=utf-8
#author:Hao Jiang
#homework09
import unittest
import os,prettytable
from prettytable import PrettyTable
from collections import defaultdict

class Student: #record students information
    def __init__(self , s_cwid , s_name , s_majior):
        self.s_cwid = s_cwid
        self.s_name = s_name
        self.s_major = s_majior
        self.s_coursegrade ={}
    
    def get_coursegrade(self , course , grade):
        self.s_coursegrade[course] = grade

    def studentsummary(self):
        return [self.s_cwid , self.s_name , sorted(self.s_coursegrade.keys()) ]

class Instructor: #record teacher information
    def __init__(self , i_cwid , i_name , i_department):
        self.i_cwid = i_cwid
        self.i_name = i_name
        self.i_department = i_department
        self.i_studentnum = defaultdict(int)

    def count_studentsnum(self,course): #the student num
        self.i_studentnum[course] += 1

    def instructorsummary(self):
        for course, studentnum in  self.i_studentnum.items():
            return[ self.i_cwid , self.i_name , self.i_department , course , self.i_studentnum ]

class FileAnalyzer:
    def __init__(self, directory: str) -> None:
        self.directory: str = directory
        self.studentdict = {}
        self.instructordict = {}
        self.student(os.path.join(directory,'student.txt'))
        self.instructor(os.path.join(directory,'instructors.txt'))
        self.gradesget(os.path.join(directory,'grades.txt'))
    
    def student(self,path): #open file and create a dictionary
        try:
            s_file = open(path,'r')
        except FileNotFoundError:
            print('There is some thing wrong about opening this file ')
        else:
            if os.stat('student.txt').st_size == 0:
                raise ValueError('This file is empty')
            else:
                s_file.seek(0)
                for line in s_file:
                    self.s_cwid , self.s_name , self.s_major = line.strip().split('\t')
                    self.studentdict[s_cwid] = Student(s_cwid , s_name , s_major)

    def instructor(self,path): #open file and create a dictionary
        try:
            i_file = open(path,'r')
        except FileNotFoundError:
            print('There is some thing wrong about opening this file ')
        else:
            if os.stat('instructors.txt').st_size == 0:
                raise ValueError('This file is empty')
            else:
                i_file.seek(0)
                for line in i_file:
                    self.i_cwid , self.i_name , self.i_department = line.strip().split('\t')
                    self.instructordict[i_cwid] = Instructor(self.i_cwid , self.i_name , self.i_department)

    def gradesget(self,path) : #open file and create a dictionary
        try:
            g_file = open(path,'r')
        except FileNotFoundError:
            print('There is some thing wrong about opening this file ')
        else:
            if os.stat('grades.txt').st_size == 0:
                raise ValueError('This file is empty')
            else:
                g_file.seek(0)
                lines = g_file.strip()
                for line in lines:
                    s_cwid , s_course , g_grade , i_cwid = line.split('/t')
                    if s_cwid in self.studentdict:
                        self.studentdict[s_cwid].get_coursegrade()
                    else:
                        raise ValueError('find unknown student')
                    if i_cwid in self.instructordict:
                        self.instructordict[i_cwid].count_studentsnum()
                    else:
                        raise ValueError('find unknown teacher')
            
    def pretty_print(self) -> None: #Print all students and instructors prettytable
        pt : PrettyTable = PrettyTable(field_names=["CWID","NAME","Completed Course"])
        for i in  self.studentdict.items():
            pt.add_row(i)
        print (pt)
        tb : PrettyTable = PrettyTable(field_names=["CWID","NAME","Dept","Course","Students"])
        for p in  self.instructordict.items():
            tb.add_row(p)
        print (tb)
         
def main():
    repo = FileAnalyzer(directory)
    repo.pretty_print()

if __name__ == '__main__':
    main()