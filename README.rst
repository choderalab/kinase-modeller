===============
Kinase Modeling
===============


.. image:: https://img.shields.io/pypi/v/kinase_modeling.svg
        :target: https://pypi.python.org/pypi/kinase_modeling

.. image:: https://img.shields.io/travis/steven-albanese/kinase_modeling.svg
        :target: https://travis-ci.org/steven-albanese/kinase_modeling

.. image:: https://readthedocs.org/projects/kinase-modeling/badge/?version=latest
        :target: https://kinase-modeling.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Package to extract kinase features from physical modeling


* Free software: MIT license
* Documentation: https://kinase-modeling.readthedocs.io.


Features
--------

When given a PDB code plus a chain index, this script collect information including (1) the kinase ID, (2) the standard name, (3) the KLIFS-defined structure ID, (4) the KLIFS-defined sequence of 85 binding pocket residues (http://klifs.vu-compmedchem.nl/index.php), (5) the indices of the 85 residues in the corresponding structure, and (6) residue indices involved in collective variables for kinase conformational changes and ligand interactions.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
