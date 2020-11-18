#coding=utf-8
#author:Hao Jiang
#homework09 test
import unittest
import os,prettytable
from prettytable import PrettyTable
from collections import defaultdict
from HW09_Hao_Jiang import FileAnalyzer,Student,Instructor
class StudentsTest(unittest.TestCase):
    def tset_studentsummary(unittest.TestCase):
        self.assertEqual(student.studentsummary(), ['11788', 'Forbes, I', ['SSW 555' , 'SSW 567']])


class InstructorTest(unittest.TestCase):
    def tset_instructorsummary(unittest.TestCase):
    self.assertEqual(instructor.instructorsummary(), ['98764', 'Feynman, R', 'SFEN' , 'SSW687' , '3'])


class FileAnalyzerTest(unittest.TestCase):  
    def tset_FileAnalyzer(unittest.TestCase):
        repo = FileAnalyzer(directory)
        repo.pretty_print()



if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
    