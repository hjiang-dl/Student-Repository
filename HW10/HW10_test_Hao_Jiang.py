#coding=utf-8
#author:Hao Jiang
#homework10 test
from typing import Tuple, Iterator,List
import unittest
import os,prettytable
from prettytable import PrettyTable
from collections import defaultdict
from HW10_Hao_Jiang import file_reader,Student,Instructor,FileAnalyzer
class InstructorTest(unittest.TestCase):
    def tset_instructorsummary(unittest.TestCase):
        self.assertEqual(instructor.instructorsummary(), ['98764', 'Feynman, R', 'SFEN' , 'SSW687' , '3'])

class StudentsTest(unittest.TestCase):
    def tset_studentsummary(unittest.TestCase):
        self.assertEqual(student.studentsummary(), ['11788', 'Forbes, I', ['SSW 555' , 'SSW 567'] ,['SSW 540' , 'SSW 564'] ,['cs 501' , 'cs 513' , 'cs 545'] , '3.88'])
    def test_major(unittest.TestCase):
        self.assertEqual(majors(),['SFEN' , ['SSW540' ,'SSW555','SSW564','SSW567'] , ['CS501','CS513','CS545']])
        
class FileAnalyzerTest(unittest.TestCase):  
    def tset_FileAnalyzer(unittest.TestCase):
        repo = FileAnalyzer(directory)
        repo.pretty_print()



if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)