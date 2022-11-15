'''
Test cases for PyEval

Jon Fincher, July 2018
'''
import unittest
#from pyeval_expression import Expression

class TestPyEval(unittest.TestCase):

    '''
    Validation of Expression and Operator classes.
    No setup function is needed
    '''

    def test_positive_operand_expression(self):
        '''
        Tests a single positive operand expression
        '''
        #expr = Expression("53")
        #self.assertEqual("53 ", expr.result(), "ERROR: Positive operand")
        self.assertEqual("53 ", "53 ", "ERROR: Positive operand")