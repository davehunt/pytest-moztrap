__version__ = '0.1a'

test_cases = {}

def pytest_addoption(parser):
    group = parser.getgroup('caseconductor', 'caseconductor')
    group._addoption('--cc-url',
                     action='store',
                     dest='cc_url',
                     default='http://caseconductor.mozilla.org',
                     metavar='url',
                     help='url for the case conductor instance')
    group._addoption('--cc-username',
                     action='store',
                     dest='cc_username',
                     metavar='str',
                     help='case conductor username')
    group._addoption('--cc-password',
                     action='store',
                     dest='cc_password',
                     metavar='str',
                     help='case conductor password')
    group._addoption('--cc-product',
                     action='store',
                     dest='cc_product',
                     metavar='str',
                     help='product identifier')
    group._addoption('--cc-cycle',
                     action='store',
                     dest='cc_cycle',
                     metavar='str',
                     help='test cycle identifier')
    group._addoption('--cc-run',
                     action='store',
                     dest='cc_run',
                     metavar='str',
                     help='test run identifier')
    group._addoption('--cc-suite',
                     action='store',
                     dest='cc_suite',
                     metavar='str',
                     help='test suite identifiers (comma separated)')
    group._addoption('--cc-coverage',
                     action='store',
                     dest='cc_coverage',
                     metavar='str',
                     help='show the coverage report')


def pytest_configure(config):
    config.addinivalue_line(
        'markers', 'cc(*ids): associate Case Conductor test cases with the test.')


def pytest_terminal_summary(terminalreporter):
    config = terminalreporter.config
    if not test_cases or config.option.verbose < 1:
        return
    tw = terminalreporter._tw
    tw.sep('-', 'Case Conductor')

    for k, v in test_cases.items():
        #TODO use the Case Conductor API to get the description of the test case
        tw.line('%s: %s' % (k, v))


def pytest_runtest_makereport(__multicall__, item, call):
    report = __multicall__.execute()
    if report.when == 'call':
        if hasattr(item.obj, 'cc'):
            _marker = getattr(item.obj, 'cc')
            _ids = _marker.args[0]
            if not isinstance(_ids, list):
                _ids = [_ids]
            for x in _ids:
                if report.skipped:
                    continue
                if not test_cases.has_key(x) or report.failed:
                    test_cases[x] = report.outcome.upper()
    return report
