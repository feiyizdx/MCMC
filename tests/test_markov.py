#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_markov
----------------------------------

Tests for `markov` module.
"""

import sys
import unittest


from markov.markov import *

class Testmarkov(unittest.TestCase):
     # test weights cal function
     def test_weights(self):
        self.assertEquals(cacl_weights(0.0, 1.0, 0.0, 2.0), 1.0)
    #test the idea of distance calculation function 
     def test_coordine(self):
         self.assertEquals(cacl_weights(xv[xrange[1],yrange[1]], yv[xrange[1],yrange[1]],xv[xrange[1],yrange[1]], yv[xrange[1],yrange[1]]),0)
    #test the use of shortest path length is not wrong.
     def test_len(self):
         self.assertEqual(nx.shortest_path_length(FG,source=2,target=2, weight='weight'),0)
    #test initial class works or not. check the code whether stores the node #1 x coord as 3.
     def test_initial(self):
         self.assertEqual(xrange[1],1)
    #test expected edges  after add
     def test_addedge(self):
         num1=FG.number_of_edges()
         add_func()
         num2=FG.number_of_edges()
         self.assertEqual(num2-num1,1)
    #test expected edges after cut
     def test_cutedge(self):
         num1=FG.number_of_edges()
         cut_func()
         num2=FG.number_of_edges()
         self.assertEqual(num2-num1,-1)
  


if __name__ == '__main__':
    sys.exit(unittest.main())
  # assert 'GitHub' in BeautifulSoup(response.content).title.string
