"""
run "python setup.py develop" before running the contained test
"""
import py

pytest_plugins = 'pytester'

def test_summary_is_not_output_when_no_id_in_marker(testdir):
    testdir.makepyfile("""
        def test_whatever():
            pass
        """)
    result = testdir.runpytest('--verbose')
    assert result.ret == 0
    py.test.raises(Exception, result.stdout.fnmatch_lines, ['*MozTrap*'])

def test_summary_when_single_id_in_marker(testdir):
    testdir.makepyfile("""
        import pytest
        @pytest.mark.moztrap(1234)
        def test_whatever():
            pass
        """)
    result = testdir.runpytest('--verbose')
    assert result.ret == 0
    result.stdout.fnmatch_lines(['*MozTrap*',
                                 '1234*'])

def test_summary_when_multiple_ids_in_marker(testdir):
    testdir.makepyfile("""
        import pytest
        @pytest.mark.moztrap([1234, 1235])
        def test_whatever():
            pass
        """)
    result = testdir.runpytest('--verbose')
    assert result.ret == 0
    result.stdout.fnmatch_lines(['*MozTrap*',
                                 '1234*',
                                 '1235*'])

def test_duplicate_ids_in_a_single_test_are_removed_from_summary(testdir):
    testdir.makepyfile("""
        import pytest
        @pytest.mark.moztrap([1234, 1234])
        def test_whatever():
            pass
        """)
    result = testdir.runpytest('--verbose')
    assert result.ret == 0
    result.stdout.fnmatch_lines(['*MozTrap*',
                                 '1234*'])
    assert str(result.outlines).count('1234:') == 1

def test_duplicate_ids_across_tests_are_removed_from_summary(testdir):
    testdir.makepyfile("""
        import pytest
        @pytest.mark.moztrap([1234])
        def test_whatever1():
            pass
        @pytest.mark.moztrap([1234])
        def test_whatever2():
            pass
        """)
    result = testdir.runpytest('--verbose')
    assert result.ret == 0
    result.stdout.fnmatch_lines(['*MozTrap*',
                                 '1234*'])
    assert str(result.outlines).count('1234:') == 1

def test_duplicate_ids_across_tests_are_removed_from_summary_and_failure_takes_priority(testdir):
    testdir.makepyfile("""
        import pytest
        @pytest.mark.moztrap([1234])
        def test_whatever1():
            pass
        @pytest.mark.moztrap([1234])
        def test_whatever2():
            assert False
        """)
    result = testdir.runpytest('--verbose')
    assert result.ret == 1
    result.stdout.fnmatch_lines(['*MozTrap*',
                                 '1234: FAILED'])
    assert str(result.outlines).count('1234:') == 1

def test_duplicate_ids_across_tests_are_removed_from_summary_and_failure_takes_priority_when_final_outcome_is_passed(testdir):
    testdir.makepyfile("""
        import pytest
        @pytest.mark.moztrap([1234])
        def test_whatever1():
            assert False
        @pytest.mark.moztrap([1234])
        def test_whatever2():
            pass
        """)
    result = testdir.runpytest('--verbose')
    assert result.ret == 1
    result.stdout.fnmatch_lines(['*MozTrap*',
                                 '1234: FAILED'])
    assert str(result.outlines).count('1234:') == 1

def test_summary_does_not_contain_ids_for_skipped_tests(testdir):
    testdir.makepyfile("""
        import pytest
        @pytest.mark.moztrap([1234])
        def test_whatever():
            pytest.skip()
        """)
    result = testdir.runpytest('--verbose')
    assert result.ret == 0
    py.test.raises(Exception, result.stdout.fnmatch_lines, ['*MozTrap*'])
