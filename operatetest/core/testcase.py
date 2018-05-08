import contextlib
import unittest

import sys, re,os

import time

import datetime

from ..auxiliary import VAR
from ..utils import Logger
from .report import generate_case_report

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
            return "pass"
        for test, exc_info in self.errors:
            if exc_info is not None:
                if issubclass(exc_info[0], AssertionError):
                    return "fail"
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

    def init(self):
        self.case_name = self.__class__.__name__
        self.log = Logger.get_logger(self.case_name)

        # self.ad = getattr(VAR, "ad")
        # setattr(self.ad, "log", self.log)

        self.startTime = datetime.datetime.now()
        VAR.cur_case_name = self.case_name
        s = sys.modules[self.__module__]
        self.log.info(s.__file__)
        self.parse_doc(s.__doc__)
        self.report_dir = os.path.join(VAR.report_dir,self.case_name)
        self.screen_shot_dir = os.path.join(self.report_dir, "image")
        VAR.screen_shot_dir = self.screen_shot_dir
        os.makedirs(self.report_dir,exist_ok=True)
        if VAR.screen_shot in ["true","True",]:
            os.makedirs(self.screen_shot_dir, exist_ok=True)

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

            self.log.info("------------------------------------ {} setUp start  -------------------------------------".format(self.case_name), setUp_start=True)
            with outcome.testPartExecutor(self):
                try:
                    self.setUp()
                except Exception as e:
                    self.log.exception(e)
                    raise e
            if outcome.success:
                self.log.info("------------------------------------ {} setUp end  ---------------------------------------".format(self.case_name), setUp_end=True)
            else:
                self.log.error("----------------------------------- {} setUp end  ---------------------------------------".format(self.case_name), setUp_end=True)

            time.sleep(0.2)
            if outcome.success:
                outcome.expecting_failure = expecting_failure
                self.log.info("------------------------------------ {} test start  --------------------------------------".format(self.case_name),test_start=True)
                with outcome.testPartExecutor(self, isTest=True):
                    try:
                        testMethod()
                    except Exception as e:
                        self.log.exception(e)
                        raise e
                if outcome.success:
                    self.log.info("------------------------------------ {} test end  ----------------------------------------".format(self.case_name),test_end=True)
                else:
                    self.log.error("------------------------------------ {} test end  ----------------------------------------".format(self.case_name),test_end=True)

                outcome.expecting_failure = False

                time.sleep(0.2)
                self.log.info("------------------------------------ {} tearDown start  ----------------------------------".format(self.case_name),tearDown_start=True)

                is_teardown_success=True
                with outcome.testPartExecutor(self):
                    try:
                        self.tearDown()
                    except Exception as e:
                        is_teardown_success = False
                        self.log.exception(e)
                        raise e
                if is_teardown_success:
                    self.log.info("------------------------------------ {} tearDown end  ------------------------------------".format(self.case_name),tearDown_end=True)
                else:
                    self.log.error("------------------------------------ {} tearDown end  ------------------------------------".format(self.case_name), tearDown_end=True)

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
            if outcome.testResult == "pass":
                self.log.info("------------------------------------ TestCase {} PASS  ------------------------------------".format(self.case_name),teseCase_end=True)
            else:
                self.log.error("------------------------------------ TestCase {} {}  ------------------------------------".format(self.case_name,outcome.testResult.upper()),teseCase_end=True)
            self.collect_something(outcome,result)
            result.testCases.append(self) # add by yang
            generate_case_report(self)
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
    def collect_something(self, outcome,result):
        self.stopTime = datetime.datetime.now()
        self.testResult = outcome.testResult
        self.timeTaken = result.getTimeTaken(self.stopTime,self.startTime)
        self.startTime = str(self.startTime)[:-7]
        self.stopTime = str(self.stopTime)[:-7]
        self.report_href = "{}/{}.html".format(self.case_name,self.case_name)

        if not outcome.success:
            for i in outcome.errors:
                if i[1]:
                    t = i[1]
                    self.message = "{}：{}".format(str(t[0])[8:-2],t[1])
                    break

    def parse_doc(self, doc):
        """从当前用例doc解析出用例信息,如Title"""
        ret = re.search(r'@Title：(.*)', doc)
        if ret:
            self.case_title = ret.group(1)
