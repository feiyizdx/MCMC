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
* the input parameters are steps (istep), weights realted parameter T and r (T, r), total nodes number (m), the nodes location in the 2-D grid (init.coor([_,_,...], [_,_,...]))
Features
--------
* This is a Markov Chain Monte Carlo code for CHE477 project
* The code employs Metropolis-Hastings Alogotithm
* The proposal probality is based on randomly cuting/adding an edge

####Proposal probality
There are three cases, cannot cut case, cannot add case and normal case.

1. Cannot cut case. If the graph is disconnected by cutting any edges, it cannot cut case.
 The probality of adding an edge is 1. 
 1. P(j|i)=1/(total possible edges - edges already exist).
 2. We need to cut an edge to go back to previous graph. If after adding, it becomes cannot add case. P(i|j)=1/(edges exist - edges cannot be cut). If after adding, it is a normal case. P(i|j)=0.5/(edges exist - edges cannot be cut)

2. Cannot add case. If the graph cannot add any more edges, it cannot add case. 
The probality of removing an edge is 1.
 1. P(j|i)=1/(edges exist - edges cannot be removed)
 2. We need to add an edge to go back to previous graph. If after cutting, it becomes cannot cut case. P(i|j)=1/(total possible edges - edges already exist). If it's normal case, P(i|j)=1/(total possible edges - edges already exist). 

3. Normal case. The probality of adding or removing is 0.5.
 If add an edge, P(j|i)=1/(total possible edges - edges already exist).
 If cut an edge, P(j|i)=1/(edges exist - edges cannot be removed)
 The calculation of P(i|j) is similar to previous cases.



Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

