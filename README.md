# pytest-caseconductor

pytest-caseconductor is a plugin for [py.test](http://pytest.org/) that
provides integration with Mozilla's Case Conductor test case management tool.

**NOTE: This plugin is currently in the very early development stage, and very
little functionality has been implemented. For a list of Case Conductor test
cases and their outcome use the `--verbose` command line option.**

## Continuous Integration

[![Build Status](https://secure.travis-ci.org/davehunt/pytest-caseconductor.png?branch=master)](http://travis-ci.org/davehunt/pytest-caseconductor)

## Installation

    $ python setup.py install

## Running

For full usage details run the following command:

    $ py.test --help

    caseconductor:
      --cc-url=url        url for the case conductor instance
      --cc-username=str   case conductor username
      --cc-password=str   case conductor password
      --cc-product=str    product identifier
      --cc-cycle=str      test cycle identifier
      --cc-run=str        test run identifier
      --cc-suite=str      test suite identifiers (comma separated)
      --cc-coverage=str   show the coverage report

## Marking tests

To indicate related test cases, use the Case Conductor mark as follows:

### Example (single related test case)

    import pytest
    @pytest.mark.cc(1000)
    def test_stuff_works():
        assert stuff_works

### Example (multiple related test cases)

    import pytest
    @pytest.mark.cc([1001, 1002])
    def test_stuff_works():
        assert stuff_works
