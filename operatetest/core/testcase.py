import contextlib
import unittest

import sys, re

import time

from ..auxiliary import VAR
from ..utils import Logger

__all__ = ["TestCase"]


class SkipTest(Exception):
    """
    Raise this exception in a test to skip it.

    Usually you can use TestCase.skipTest() or one of the skipping decorators
    instead of raising this directly.
    """


class _ShouldStop(Exception):
    """
    The test should stop.
    """


class _Outcome(object):
    def __init__(self, result=None):
        self.expecting_failure = False
        self.result = result
        self.result_supports_subtests = hasattr(result, "addSubTest")
        self.success = True
        self.skipped = []
        self.expectedFailure = None
        self.errors = []

    # add by yang
    @property
    def testResult(self):
        if self.success:
            return "passed"
        for test, exc_info in self.errors:
            if exc_info is not None:
                if issubclass(exc_info[0], AssertionError):
                    return "failed"
                else:
                    return "error"

    @contextlib.contextmanager
    def testPartExecutor(self, test_case, isTest=False):
        old_success = self.success
        self.success = True
        try:
            yield
        except KeyboardInterrupt:
            raise
        except SkipTest as e:
            self.success = False
            self.skipped.append((test_case, str(e)))
        except _ShouldStop:
            pass
        except:
            exc_info = sys.exc_info()
            if self.expecting_failure:
                self.expectedFailure = exc_info
            else:
                self.success = False
                self.errors.append((test_case, exc_info))
            # explicitly break a reference cycle:
            # exc_info -> frame -> exc_info
            exc_info = None
        else:
            if self.result_supports_subtests and self.success:
                self.errors.append((test_case, None))
        finally:
            self.success = self.success and old_success


class TestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.case_name = self.__class__.__name__
        self.log = Logger.get_logger(self.case_name)

        # self.ad = getattr(VAR, "ad")
        # setattr(self.ad,"log",self.log)

    def init(self):
        self.startTime = time.time()
        VAR.cur_case_name = self.case_name
        s = sys.modules[self.__module__]
        self.log.info(s.__file__)
        self.parse_doc(s.__doc__)

    def run(self, result=None):
        self.init()
        orig_result = result
        if result is None:
            result = self.defaultTestResult()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()

        result.startTest(self)

        testMethod = getattr(self, self._testMethodName)
        if (getattr(self.__class__, "__unittest_skip__", False) or
                getattr(testMethod, "__unittest_skip__", False)):
            # If the class or method was skipped.
            try:
                skip_why = (getattr(self.__class__, '__unittest_skip_why__', '')
                            or getattr(testMethod, '__unittest_skip_why__', ''))
                self._addSkip(result, self, skip_why)
            finally:
                result.stopTest(self)
            return
        expecting_failure_method = getattr(testMethod,
                                           "__unittest_expecting_failure__", False)
        expecting_failure_class = getattr(self,
                                          "__unittest_expecting_failure__", False)
        expecting_failure = expecting_failure_class or expecting_failure_method
        outcome = _Outcome(result)
        try:
            self._outcome = outcome

            with outcome.testPartExecutor(self):
                self.log.info("------------------------------ {} setUp start  -------------------------------".format(
                    self.case_name))
                try:
                    self.setUp()
                except Exception as e:
                    self.log.exception(e)
                    raise e
                finally:
                    self.log.info(
                        "------------------------------ {} setUp end  ------------------ --------------".format(
                            self.case_name))
            if outcome.success:
                outcome.expecting_failure = expecting_failure
                with outcome.testPartExecutor(self, isTest=True):
                    self.log.info(
                        "------------------------------ {} test start  --------------------------------".format(
                            self.case_name))
                    try:
                        testMethod()
                    except Exception as e:
                        self.log.exception(e)
                        raise e
                    finally:
                        self.log.info(
                            "------------------------------ {} test end  ----------------------------------".format(
                                self.case_name))
                outcome.expecting_failure = False
                with outcome.testPartExecutor(self):
                    self.log.info(
                        "------------------------------ {} tearDown start  ----------------------------".format(
                            self.case_name))
                    try:
                        self.tearDown()
                    except Exception as e:
                        self.log.exception(e)
                        raise e
                    finally:
                        self.log.info(
                            "------------------------------ {} tearDown end  ------------------------------".format(
                                self.case_name))
            self.doCleanups()
            for test, reason in outcome.skipped:
                self._addSkip(result, test, reason)
            self._feedErrorsToResult(result, outcome.errors)
            if outcome.success:
                if expecting_failure:
                    if outcome.expectedFailure:
                        self._addExpectedFailure(result, outcome.expectedFailure)
                    else:
                        self._addUnexpectedSuccess(result)
                else:
                    result.addSuccess(self)
            self.collect_something(outcome)
            return result
        finally:
            result.stopTest(self)
            if orig_result is None:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()

            # explicitly break reference cycles:
            # outcome.errors -> frame -> outcome -> outcome.errors
            # outcome.expectedFailure -> frame -> outcome -> outcome.expectedFailure
            outcome.errors.clear()
            outcome.expectedFailure = None

            # clear the outcome, no more needed
            self._outcome = None

    # ----add begin----
    def collect_something(self, outcome):
        self.stopTime = time.time()
        self.timeTaken = self.stopTime - self.startTime
        self.testResult = outcome.testResult
        print(self.startTime,self.stopTime,self.timeTaken,self.testResult)

    def parse_doc(self, doc):
        """从当前用例doc解析出用例信息,如Title"""
        ret = re.search(r'@Title：(.*)', doc)
        if ret:
            self.title = ret.group(1)
