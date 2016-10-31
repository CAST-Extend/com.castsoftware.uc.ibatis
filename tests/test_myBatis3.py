'''
Created on 31 mai 2016

@author: MMR
'''
import unittest
from cast.analysers.test import JEETestAnalysis

class Test(unittest.TestCase):


    def test_xml(self):     
        analysis = JEETestAnalysis()
        analysis.add_selection('test_mybatis3')
        analysis.set_verbose()
        analysis.add_database_table('PMDCUSMO', 'TSQL')
        analysis.run()

if __name__ == "__main__":
    unittest.main()