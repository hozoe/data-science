import unittest
from pathlib import Path
import os, sys

from src.compile_word_counts import *
from src.compute_pony_lang import sort_tdidf
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)


class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')
        self.stopwords = os.path.join(dir,'..','data','stopwords.txt')
        print("\nRUNNING TESTS FOR test_tasks.py")

        

    def test_task1(self):
        # use  self.mock_dialog and self.true_word_counts; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        print(f"Ensure word count task performs correctly")
        stopwords = get_stopwords(self.stopwords)
        counts = compute_counts(preprocess(self.mock_dialog,stopwords))
        res = keep_frequency(counts)
        with open(self.true_word_counts,'r') as f:
            self.assertEqual(res,json.load(f))
        print("OK\n")
    
    def test_task2(self):
        # use self.true_word_counts self.true_tf_idfs; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        print(f"Ensure tdidf is calculated correctly \n")
        with open(self.true_word_counts,'r') as f:
            data = json.load(f)
            res = sort_tdidf(data,3)
        with open(self.true_tf_idfs, 'r') as ff:
            self.assertEqual(res,json.load(ff))

        print("OK\n")
        
    
if __name__ == '__main__':
    unittest.main()