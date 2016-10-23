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
* the input parameters are steps: nstep, weights realted parameter T and r, total nodes number: m, the :

Features
--------

Proposal probality
--------
* If the graph is disconnected by cutting any edges. the probality of adding an edge is 1. 
* If the graph cannot add any more edges, the probality of removing an edge is 1.
* Otherwise. The probality of adding or removing is 0.5.


* TODO

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

