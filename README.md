# pytest-moztrap

pytest-moztrap is a plugin for [py.test](http://pytest.org/) that
provides integration with Mozilla's MozTrap test case management tool.

**NOTE: This plugin is currently in the very early development stage, and very
little functionality has been implemented. For a list of MozTrap test
cases and their outcome use the `--verbose` command line option.**

## Continuous Integration

[![Build Status](https://secure.travis-ci.org/davehunt/pytest-moztrap.png?branch=master)](http://travis-ci.org/davehunt/pytest-moztrap)

## Installation

    $ python setup.py install

## Running

For full usage details run the following command:

    $ py.test --help

    moztrap:
      --mt-url=url        url for the moztrap instance
      --mt-username=str   moztrap username
      --mt-password=str   moztrap password
      --mt-product=str    product identifier
      --mt-cycle=str      test cycle identifier
      --mt-run=str        test run identifier
      --mt-suite=str      test suite identifiers (comma separated)
      --mt-coverage=str   show the coverage report

## Marking tests

To indicate related test cases, use the MozTrap mark as follows:

### Example (single related test case)

    import pytest
    @pytest.mark.moztrap(1000)
    def test_stuff_works():
        assert stuff_works

### Example (multiple related test cases)

    import pytest
    @pytest.mark.moztrap([1001, 1002])
    def test_stuff_works():
        assert stuff_works
