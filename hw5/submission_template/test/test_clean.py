import unittest
from pathlib import Path
import os, sys
import os.path as osp
import json
from src.clean import createdat_to_utc, format_title, remove_author, split_tags, total_count_to_int, valid_json
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)


class CleanTest(unittest.TestCase):
    def setUp(self):
        # You might want to load the fixture files as variables, and test your code against them. Check the fixtures folder.
        self.clean_file_path = osp.join(parentdir, 'src', 'clean.py')
        self.path1 = osp.join(parentdir, 'test', 'fixtures', 'test_1.json')
        self.path2 = osp.join(parentdir, 'test', 'fixtures', 'test_2.json')
        self.path3 = osp.join(parentdir, 'test', 'fixtures', 'test_3.json')
        self.path4 = osp.join(parentdir, 'test', 'fixtures', 'test_4.json')
        self.path5 = osp.join(parentdir, 'test', 'fixtures', 'test_5.json')
        self.path6 = osp.join(parentdir, 'test', 'fixtures', 'test_6.json')
        #self.path7 = osp.join(parentdir, 'test', 'fixtures', 'test_7.json')
        self.assertEqual(os.path.isfile(self.clean_file_path), True)
    
    #test_1.json
    def test_title(self):
        print("\nRUNNING TESTS FOR HW5 - clean.format_title(post)")
        expected = None
        with open(self.path1, 'r') as file:
            for l in file:
                myres = format_title(json.loads(l))
        self.assertEqual(expected,myres)
        print("OK")
        #print("format_title done")
    
    #test_2.json
    def test_createdAt(self):
        print("\nRUNNING TESTS FOR HW5 - clean.createdat_to_utc(post)")
        expected = None
        with open(self.path2, 'r') as file:
            for l in file:
                myres = createdat_to_utc(json.loads(l))
        self.assertEqual(expected,myres)
        print("OK")
    
    #test_3.json
    def test_valid_json(self):
        print("\nRUNNING TESTS FOR HW5 - clean.valid_json(post)")
        expected = None
        with open(self.path3, 'r') as file:
            for l in file:
                myres = valid_json(l)
        self.assertEqual(expected,myres)
        print("OK")

    #test_4.json
    def test_author(self):
        print("\nRUNNING TESTS FOR HW5 - clean.remove_author(post)")
        expected = None
        with open(self.path4, 'r') as file:
            for l in file:
                myres = remove_author(json.loads(l))
        
        self.assertEqual(expected,myres)
        print("OK")

    #test_5.json
    def test_total_count(self):
        print("\nRUNNING TESTS FOR HW5 - clean.total_count_to_int(post)")
        expected1 = None
        with open(self.path5, 'r') as file:
            for l in file:
                myres1 = total_count_to_int(json.loads(l))
        self.assertEqual(expected1,myres1)
        print("OK")
        # expected2 = None
        # with open(self.path7, 'r') as file:
        #     for l in file:
        #         myres2 = total_count_to_int(json.loads(l))
        
        #print("fail to cast: OK")
        #self.assertEqual(expected2,myres2)
        #print("cast flt in str to int: OK")

    #test_6.json
    def test_split_tags(self):
        print("\nRUNNING TESTS FOR HW5 - clean.split_tags(post)")
        expected = 4
        with open(self.path6, 'r') as file:
            for l in file:
                myres = split_tags(json.loads(l))
        self.assertEqual(expected,len(myres["tags"]))

    def tearDownClass():
        print("\n\nYou are all set! <3")
    
if __name__ == '__main__':
    unittest.main()