'''
Created on Dec 7, 2016

@author: JGD
'''
import unittest
import cast.analysers.test

class Test(unittest.TestCase):
    def testRegisterPlugin(self):
        # create a DotNet analysis
        analysis = cast.analysers.test.DotNetTestAnalysis()
        # DotNet need a selection of a csproj
        analysis.add_database_table('EMPLOYEE', 'Oracle')
        analysis.add_database_table('DEPARTMENT', 'Oracle')
        analysis.add_selection('MyBatisDataMapper/MyBatisDataMapper/MyBatisDataMapper.csproj')
        analysis.set_verbose()
        analysis.run()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()