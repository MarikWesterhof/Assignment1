# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 14:08:54 2018

@author: Marik
"""

# Import the necessary modules for CSV, shuffling, and unit testing.
import csv
import random
import unittest
import os

# Main function that uses four inputs:
# - # of Assignments                    ass
# - # students per group                spg
# - Name of input file                  inp
# - Name of output file                 out

# CSV -> CSV
def groupify(ass, spg, inp, out):
    
    # Obtain student list from CSV
    students = read_file(inp)
    
    # Check if group size isn't too high or low
    check_groupsize(students, spg)
    
    # Cumulative groups list
    g_cumu = []
       
    # Repeat the following for every assignment
    for i in range(ass):
        
        # Make the (unformatted) group list
        g_unform = make_lists(i, students, spg)
        
        # Format this list; make it CSV-ready       
        g_form = format_lists(i, g_unform)
        
        g_cumu.append(g_form)
              
    # Write formatted list to specified CSV
    write_file(ass, g_cumu, out)
        
        
    # Return unformatted list (for unit testing)
    return(g_unform)
        
        
# CSV -> [List of Strings]    
def read_file(inp):
        
    # Read the given CSV file name and turn it into a student info list.
    with open(inp, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        student_info = list(reader)
        
    # Skim all info but people's first names
    students = ([s[0] for s in student_info])
    
    return(students)
    

# Number, [List of Lists], String -> CSV       
def write_file(ass, g_cumu, out):
    
    # Write the now formatted list to the given CSV
    with open(out, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        for i in range(ass):
            writer.writerows(g_cumu[i])   
    
        
# Number, [List of Strings], Number -> [List of Lists]                
def make_lists(i, students, spg):
    
    # Shuffle the group list for every assignment
    random.shuffle(students)
    
    # Make lists depending on group size
    g_unform = ([students[i:i + spg] for i in range(0, len(students), spg)])
    
    # Check for if the last group is >1 smaller than the others and fix it
    g_unform = divide_leftovers(g_unform)
        
    return(g_unform)
    
    
# Number, [List of Lists] -> [List of Lists]   
def format_lists(i, g_unform):
    
    # Firstly, a line for "Assignment #"
    g_form = []
    g_form.append(['Assignment ' + str(i + 1)])
                  
    # Secondly, a loop that writes the groups out for each assignment
    for i in range(len(g_unform)):
        g_form.append(g_unform[i])
        
    # Thirdly, a blank line between assignments for tidiness
    g_form.append('\n')
    
    return(g_form)
  
    
# [List of Lists] -> [List of Lists]     
def divide_leftovers(g_unform):
    
    # Group size difference can't be more than one. If so:
    if len(g_unform[-1]) < (len(g_unform[0])-1):
        
        # Some groups can't be split. If so, this check catches it
        check_groupdiff(g_unform)
        
        # Take the last, smaller list, and seperate it as the 'leftover list'
        g_unform, leftover = g_unform[:-1], g_unform[-1]
        
        # divide this leftover list among the other groups
        for i in range(len(leftover)):
            g_unform[i].append(leftover[i])
            
    
    return(g_unform)
    
   
# [List of Strings], Number -> Exception OR None  
def check_groupsize(students,spg):
    
    # Raise exception if given group size is too big...
    if spg > len(students):
        raise Exception('Group size given exceeds amount of students.')
    
    # ... or too small.
    elif spg < 1:
        raise Exception('Group size has to be at least one.')
        
    
# [List of Lists] -> Exception OR None       
def check_groupdiff(g_unform):
    
    # Raise exception if group sizedifference is > 1
    if len(g_unform[-1]) > len(g_unform[:-1]):
        raise Exception('Group size difference would too big')

        
        
# Unittests. Writes to att.csv as to not overwrite the normal CSV
class TestPM(unittest.TestCase):
    
    def setUp(self):
        pass
    
    ### Testing the main function
    # Splitting up the group of 23 into groups of 5 should return
    # four groups of length [6, 6, 6, 5]: this is tested as such.
    def test_groupify_groups(self):
        self.assertEqual(len(groupify(1,5,'students.csv','att.csv')),4)
        
    def test_groupify_length0(self):
        self.assertEqual(len(groupify(1,5,'students.csv','att.csv')[0]),6)
        
    def test_groupify_length1(self):
        self.assertEqual(len(groupify(1,5,'students.csv','att.csv')[1]),6)
        
    def test_groupify_length2(self):
        self.assertEqual(len(groupify(1,5,'students.csv','att.csv')[2]),6)
        
    def test_groupify_length3(self):
        self.assertEqual(len(groupify(1,5,'students.csv','att.csv')[3]),5)
    
    # Test format_lists function
    def test_format_lists(self):
        self.assertEqual(format_lists(3, ['Casper', 'Daniel']),
                         [['Assignment 4'],'Casper','Daniel','\n'])
        
    # test exception check for group size
    def test_check_groupsize_high(self):
        self.assertRaises(Exception,check_groupsize, ['Casper','Daniel'], 3)
        
    def test_check_groupsize_low(self):
        self.assertRaises(Exception,check_groupsize, ['Casper','Daniel'], 0)
        
    # test exception check for group size difference
    def test_check_groupdiff(self):
        self.assertRaises(Exception,check_groupdiff,[['a','b'],
                                                     ['c','d']],
                                                     ['e','f','g'])
        
        
if __name__ == '__main__':
    unittest.main()
 
    
# Clean up the CSV file used for testing afterwards.
os.remove('att.csv')