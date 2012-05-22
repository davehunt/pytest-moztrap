__version__ = '0.1a'

test_cases = {}

def pytest_addoption(parser):
    group = parser.getgroup('moztrap', 'moztrap')
    group._addoption('--mt-url',
                     action='store',
                     dest='moztrap_url',
                     default='http://moztrap.mozilla.org',
                     metavar='url',
                     help='url for the moztrap instance')
    group._addoption('--mt-username',
                     action='store',
                     dest='moztrap_username',
                     metavar='str',
                     help='moztrap username')
    group._addoption('--mt-password',
                     action='store',
                     dest='moztrap_password',
                     metavar='str',
                     help='moztrap password')
    group._addoption('--mt-product',
                     action='store',
                     dest='moztrap_product',
                     metavar='str',
                     help='product identifier')
    group._addoption('--mt-cycle',
                     action='store',
                     dest='moztrap_cycle',
                     metavar='str',
                     help='test cycle identifier')
    group._addoption('--mt-run',
                     action='store',
                     dest='moztrap_run',
                     metavar='str',
                     help='test run identifier')
    group._addoption('--mt-suite',
                     action='store',
                     dest='moztrap_suite',
                     metavar='str',
                     help='test suite identifiers (comma separated)')
    group._addoption('--mt-coverage',
                     action='store',
                     dest='moztrap_coverage',
                     metavar='str',
                     help='show the coverage report')


def pytest_configure(config):
    config.addinivalue_line(
        'markers', 'cc(*ids): associate MozTrap test cases with the test.')


def pytest_terminal_summary(terminalreporter):
    config = terminalreporter.config
    if not test_cases or config.option.verbose < 1:
        return
    tw = terminalreporter._tw
    tw.sep('-', 'MozTrap')

    for k, v in test_cases.items():
        #TODO use the MozTrap API to get the description of the test case
        tw.line('%s: %s' % (k, v))


def pytest_runtest_makereport(__multicall__, item, call):
    report = __multicall__.execute()
    if report.when == 'call':
        if hasattr(item.obj, 'moztrap'):
            _marker = getattr(item.obj, 'moztrap')
            _ids = _marker.args[0]
            if not isinstance(_ids, list):
                _ids = [_ids]
            for x in _ids:
                if report.skipped:
                    continue
                if not test_cases.has_key(x) or report.failed:
                    test_cases[x] = report.outcome.upper()
    return report
