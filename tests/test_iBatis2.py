'''
Created on 31 mai 2016

@author: MMR
'''
import unittest
from cast.analysers.test import JEETestAnalysis

class Test(unittest.TestCase):

    def test_xml(self):
        
        analysis = JEETestAnalysis()
        
        # mimic presence of a table in dependencies
        employee_table = analysis.add_database_table('EMPLOYEE', 'Oracle')
        
        analysis.add_selection('test_ibatis2')
        analysis.set_verbose()        
        analysis.run()

        # check that a CAST_SQL_NamedQuery named selectMyEmployees exists and contains the correct sql query
        selectMyEmployees = analysis.get_object_by_name('selectMyEmployees', 'CAST_SQL_NamedQuery')
        self.assertTrue(selectMyEmployees)

        self.assertEqual("select * from EMPLOYEE where first_name='TOTO'", 
                         getattr(selectMyEmployees, 'CAST_SQL_MetricableQuery.sqlQuery').strip())

        
        # check that there exists a useSelect link to table employee
        self.assertTrue(analysis.get_link_by_caller_callee('useSelectLink', selectMyEmployees, employee_table))
        

if __name__ == "__main__":
    unittest.main()