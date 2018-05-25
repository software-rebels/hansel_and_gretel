Hansel and Gretel
=================

Tools for detecting and removing anti-patterns in Travis CI specification (``.travis.yml``) files.

**Hansel** detects following four anti-patterns:

- Redirecting scripts into interpreters
- Bypassing security checks
- Using irrelevant properties
- Commands unrelated to the phase

**Gretel** removes the anti-pattern 4 (Commands unrelated to the phase) from ``.travis.yml`` files.

This work is published at the **IEEE Transactions on Software Engineering (TSE)** journal with the title *'Use and Misuse of Continuous Integration Features: An Empirical Study of Projects that (mis)use Travis CI'*.

If you use Hansel and Gretel in your work, please cite it as follows::

	@article{gallaba2018tse,
  		Author = {Keheliya Gallaba and Shane McIntosh},
  		Title = {{Use and Misuse of Continuous Integration Features: An Empirical Study of Projects that (mis)use Travis CI}},
  		Year = {2018},
  		Journal = {IEEE Transactions on Software Engineering},
  		Pages = {To appear}
	}

- `More about this work <http://rebels.ece.mcgill.ca/journalpaper/2018/05/15/use-and-misuse-of-continuous-integration-features.html>`_
- `Link to the paper in the IEEE library <https://doi.org/10.1109/TSE.2018.2838131>`_

Quick Start
-----------

Install the dependencies::

    $ pip install -r requirements.txt

Run all tests to make sure everything is setup properly::

    $ python -m unittest discover -v

Run the script on your own `.travis.yml` file::

    $ python hansel_and_gretel.py -p <PATH_TO_TRAVIS_YAML>


Full List of Configuration Options
----------------------------------

-h, --help            show this help message and exit
-p PATH               Path to read Travis YAML (default: test/travis_ymls/h0pre.yml)
-s SMELLS             List of smells to check (e.g. -s 1 2) Note: Checks all by default
-f, --fix             Set this for fixing the smell
-n NEW_PATH           Path to write the modified YAML file. Always use with -f
-v, --verbose         Set this to get more detailed output



