===============================
markov
===============================


.. image:: https://img.shields.io/pypi/v/markov.svg
        :target: https://pypi.python.org/pypi/markov

.. image:: https://img.shields.io/travis/xinbian/markov.svg
        :target: https://travis-ci.org/xinbian/markov

.. image:: https://readthedocs.org/projects/markov/badge/?version=latest
        :target: https://markov.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/xinbian/markov/shield.svg
     :target: https://pyup.io/repos/github/xinbian/markov/
     :alt: Updates


.. image:: https://coveralls.io/repos/github/xinbian/markov/badge.png?branch=master
      :target: https://coveralls.io/github/xinbian/markov?branch=master


Markov Chain Monte Carlo Project


* Free software: MIT license
* Documentation: https://markov.readthedocs.io.
How to use
--------
* run the code  /markov/markov.py
* the input parameters are steps (istep), weights related parameters T and r (T, r), total nodes number (m), the nodes location in the 2-D grid (init.coor([_,_,...], [_,_,...]))
* the code generates a m*m 2D grid, origin is 0, dx=dy=1. For example, if m=3, meaning we have 3 nodes and a 3*3 grid. We can initialize the nodes by init.coor([2,1,1],[1,0,1]). The first, second, and third nodes are located at (2,1), (1,0), (1,1), respectively.
Features
--------
* This is a Markov Chain Monte Carlo code for CHE477 project
* The code employs Metropolis-Hastings Algorithm
* The proposal probability is based on randomly cutting/adding an edge. There are three cases, 'cannot cut' case, 'cannot add' case and normal case.

1. 'Cannot cut' case. If the graph is disconnected by further cutting any edges, it is the so called 'cannot cut' case. Thus, the probability of adding an edge is 1. 
 1. P(j|i)=1/(total possible edges - edges already exist).
 2. We need to cut an edge to go back to previous graph. After adding an edge, if it becomes 'cannot add' case, P(i|j)=1/(existing edges - edges cannot be cut). After adding an edge, if it is a normal case, P(i|j)=0.5/(existing edges - edges cannot be cut)

2. 'Cannot add' case. If the graph cannot add any more edges, it is 'cannot add' case. The probability of removing an edge is 1.
 1. P(j|i)=1/(existing edges - edges cannot be removed)
 2. We need to add an edge to go back to previous graph. After cutting, if it becomes cannot cut case, P(i|j)=1/(total possible edges - edges already exist). If it's normal case, P(i|j)=1/(total possible edges - existing edges). 

3. Normal case. The probability of adding or removing is 0.5.
 If add an edge, P(j|i)=1/(total possible edges - existing edges).
 If cut an edge, P(j|i)=1/(existing edges - edges cannot be removed)
 The calculation of P(i|j) is similar to previous cases.

Sample results
----------
* parameters
1. 5 nodes; m=5
2. r=2, T=10
3. total steps; istep=30000
4. initial nodes position (0,0) (1,2) (1,3) (3,2) (4,4); init.coord([0,1,1,3,4],[0,2,3,2,4])

* results
1. 2 most possible graphs: graph1_ and graph2_
2. expected number of edges connected to vertex 0 is 1.97
3. expected number of edges is 4.96
4. expected maximum distance is 6.64
5. this_ shows time series of averaged quantities

.. _graph1: https://pbs.twimg.com/media/CvvhkPfXgAAm24R.jpg
.. _graph2: https://pbs.twimg.com/media/Cvvhlu3XEAAJCiF.jpg
.. _this: https://pbs.twimg.com/media/CvvbalWWEAAA3rm.jpg

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
