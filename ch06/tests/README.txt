SETUP
-----
Create a link to files being tested.

NOTE: I have not figured out how to use
relative imports correctly, so I am cheating
by setting up a link to the real file.  This
is being written and executed on a Linux PC.

ln -T ../database.py database.py


Running pytest
--------------
pytest-3 -s


Steps for creating coverage report.
-----------------------------------
1. coverage run -m pytest
2. coverage report -m
3. coverage html
4. firefox htmlcov/index.html