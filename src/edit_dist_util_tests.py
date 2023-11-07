import unittest
import pytest
from edit_dist_utils import *

class EditDistUtilTests(unittest.TestCase):
    """
    Unit tests for validating the edit dist util functionality. Notes:
    - If this is the set of tests provided in the solution skeleton, it represents an
      incomplete set that you are expected to add to to adequately test your submission!
    - Your correctness score on the assignment will be assessed by a more complete,
      grading set of unit tests.
    - A portion of your style grade will also come from proper type hints; remember to
      validate your submission using `mypy .` and ensure that no issues are found.
    """
    
    def test_edit_dist_t0(self) -> None:
        self.assertEqual(0, edit_distance("", ""))
        self.assertEqual(0, edit_distance("a", "a"))
        self.assertEqual(0, edit_distance("abc", "abc"))
        
    def test_edit_dist_t1(self) -> None:
        self.assertEqual(1, edit_distance("a", ""))
        self.assertEqual(1, edit_distance("", "a"))
        self.assertEqual(2, edit_distance("aa", ""))
        self.assertEqual(2, edit_distance("", "aa"))
        self.assertEqual(2, edit_distance("ab", "abcd"))
        
    def test_edit_dist_t2(self) -> None:
        self.assertEqual(1, edit_distance("a", "b"))
        self.assertEqual(1, edit_distance("b", "a"))
        self.assertEqual(2, edit_distance("ab", "cd"))
        self.assertEqual(3, edit_distance("cat", "dog"))
        
    def test_edit_dist_t3(self) -> None:
        self.assertEqual(1, edit_distance("ab", "ba"))
        self.assertEqual(1, edit_distance("bar", "bra"))
        
    def test_edit_dist_t4(self) -> None:
        self.assertEqual(5, edit_distance("parisss", "parsimony"))
    
    def test_edit_dist_t5(self) -> None:
        self.assertEqual(3, edit_distance("wxyyxw", "wyxxyx"))
        
    def test_edit_dist_t6(self) -> None:
        self.assertEqual(4, edit_distance("abcde", "edbca"))
        
    def test_edit_dist_t7(self) -> None:
        self.assertEqual(4, edit_distance("aaaabcde", "aaaedbca"))
        
    # Transform List Tests
    # -------------------------------------------------
    
    def test_transform_list_t0(self) -> None:
        s0 = ""
        s1 = ""
        self.assertEqual([], get_transformation_list(s0, s1))
        
    def test_transform_list_t1(self) -> None:
        s0 = "a"
        s1 = ""
        self.assertEqual(["D"], get_transformation_list(s0, s1))
        self.assertEqual(["I"], get_transformation_list(s1, s0))
        
    def test_transform_list_t2(self) -> None:
        s0 = "abc"
        s1 = ""
        self.assertEqual(["D", "D", "D"], get_transformation_list(s0, s1))
        self.assertEqual(["I", "I", "I"], get_transformation_list(s1, s0))
        
    def test_transform_list_t3(self) -> None:
        s0 = "abc"
        s1 = "bac"
        self.assertEqual(["T"], get_transformation_list(s0, s1))
        self.assertEqual(["T"], get_transformation_list(s1, s0))
        
    def test_transform_list_t4(self) -> None:
        s0 = "aaa"
        s1 = "bbb"
        self.assertEqual(["R", "R", "R"], get_transformation_list(s0, s1))
        self.assertEqual(["R", "R", "R"], get_transformation_list(s1, s0))
        
    def test_transform_list_t5(self) -> None:
        s0 = "eagle"
        s1 = "bagle"
        self.assertEqual(["R"], get_transformation_list(s0, s1))
        self.assertEqual(["R"], get_transformation_list(s1, s0))
        
    def test_transform_list_t6(self) -> None:
        s0 = "hack"
        s1 = "fkc"
        self.assertEqual(["T", "R", "D"], get_transformation_list(s0, s1))
        self.assertEqual(["T", "R", "I"], get_transformation_list(s1, s0))
        
    def test_transform_list_t7(self) -> None:
        s0 = "intuition"
        s1 = "inception"
        self.assertEqual(["R", "R", "R"], get_transformation_list(s0, s1))
        self.assertEqual(["R", "R", "R"], get_transformation_list(s1, s0))
        
    def test_transform_list_t8(self) -> None:
        s0 = "astound"
        s1 = "distant"
        self.assertEqual(["R", "R", "D", "R", "I"], get_transformation_list(s0, s1))
        self.assertEqual(["R", "R", "I", "R", "D"], get_transformation_list(s1, s0))
        
    def test_transform_list_t9(self) -> None:
        s0 = "housemaid"
        s1 = "heartsick"
        self.assertEqual(["R", "R", "R", "R", "R", "R", "R", "R"], get_transformation_list(s0, s1))
        self.assertEqual(["R", "R", "R", "R", "R", "R", "R", "R"], get_transformation_list(s1, s0))
        
    def test_transform_list_t10(self) -> None:
        s0 = "fullness"
        s1 = "fineness"
        self.assertEqual(["R", "R", "R"], get_transformation_list(s0, s1))
        self.assertEqual(["R", "R", "R"], get_transformation_list(s1, s0))
        
    def test_transform_list_t11(self) -> None:
        s0 = "axbczy"
        s1 = "abxyzc"
        self.assertEqual(["R", "R", "T"], get_transformation_list(s0, s1))
        self.assertEqual(["R", "R", "T"], get_transformation_list(s1, s0))
        
if __name__ == '__main__':
    unittest.main()