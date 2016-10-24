#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_markov
----------------------------------

Tests for `markov` module.
"""

import sys
import unittest


from markov import markov

class Testmarkov(unittest.TestCase):

  # test weights cal function
     def test_weights(self):
        self.assertEquals(cacl_weights(0.0, 1.0, 0.0, 2.0), 1.0)
    #test distance calculation
     def test_coordine(self):
         self.assertEquals(cacl_weights(xv[xrange[1],yrange[1]], yv[xrange[1],yrange[1]],xv[xrange[1],yrange[1]], yv[xrange[1],yrange[1]]),0)
    #test shortest path length
     def test_len(self):
         self.assertEqual(nx.shortest_path_length(FG,source=2,target=2, weight='weight'),0)
  


if __name__ == '__main__':
    sys.exit(unittest.main())
  # assert 'GitHub' in BeautifulSoup(response.content).title.string
