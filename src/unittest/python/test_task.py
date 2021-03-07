#   -*- coding: utf-8 -*-
import unittest
from mock import patch
from mock import call
from mock import Mock

from pybuilder_radon.task import init_radon
from pybuilder_radon.task import radon
from pybuilder_radon.task import get_command
from pybuilder_radon.task import set_verbose_property
from pybuilder_radon.task import verify_result
from pybuilder_radon.task import get_complexity
from pybuilder_radon.task import verify_complexity
from pybuilder_radon.task import process_complexity

from pybuilder.errors import BuildFailedException


class TestTask(unittest.TestCase):

    def setUp(self):
        """
        """
        pass

    def tearDown(self):
        """
        """
        pass

    def test__init_radon_Should_CallExpected_When_Called(self, *patches):
        project_mock = Mock()
        init_radon(project_mock)
        self.assertTrue(call('radon_break_build_average_complexity_threshold', None) in project_mock.set_property_if_unset.mock_calls)
        self.assertTrue(call('radon_break_build_complexity_threshold', None) in project_mock.set_property_if_unset.mock_calls)

    @patch('pybuilder_radon.task.get_command')
    @patch('pybuilder_radon.task.process_complexity')
    @patch('pybuilder_radon.task.verify_result')
    def test__radon_Should_CallExpected_When_VerifyResultFalse(self, verify_result_patch, process_complexity_patch, *patches):
        verify_result_patch.return_value = False
        project_mock = Mock()
        radon(project_mock, Mock())
        process_complexity_patch.assert_not_called()

    @patch('pybuilder_radon.task.get_command')
    @patch('pybuilder_radon.task.process_complexity')
    @patch('pybuilder_radon.task.get_complexity')
    @patch('pybuilder_radon.task.verify_result')
    def test__radon_Should_CallExpected_When_VerifyResultTrue(self, verify_result_patch, get_complexity_patch, process_complexity_patch, *patches):
        verify_result_patch.return_value = True
        project_mock = Mock()
        radon(project_mock, Mock())
        process_complexity_patch.assert_called_once_with(project_mock, get_complexity_patch.return_value)

    @patch('pybuilder_radon.task.get_command')
    @patch('pybuilder_radon.task.get_complexity')
    @patch('pybuilder_radon.task.process_complexity')
    @patch('pybuilder_radon.task.verify_complexity')
    @patch('pybuilder_radon.task.verify_result')
    def test__radon_Should_CallExpected_When_VerifyComplexityFalse(self, verify_result_patch, verify_complexity_patch, process_complexity_patch, *patches):
        verify_result_patch.return_value = True
        verify_complexity_patch.return_value = False
        project_mock = Mock()
        radon(project_mock, Mock())
        process_complexity_patch.assert_not_called()

    @patch('pybuilder_radon.task.ExternalCommandBuilder')
    def test__get_command_Should_CallAndReturnExpected_When_Called(self, external_command_builder_patch, *patches):
        project_mock = Mock()
        result = get_command(project_mock)
        external_command_builder_patch.assert_called_once_with('radon', project_mock)
        self.assertEqual(result, external_command_builder_patch.return_value)

    def test__set_verbose_property_Should_CallExpected_When_Called(self, *patches):
        project_mock = Mock()
        set_verbose_property(project_mock)
        project_mock.set_property.assert_called_once_with('radon_verbose_output', project_mock.get_property.return_value)

    def test__verify_result_Should_ReturnFalse_When_NoReportLines(self, *patches):
        result_mock = Mock()
        result_mock.report_lines = []
        result = verify_result(result_mock, Mock(), Mock())
        self.assertFalse(result)

    def test__verify_result_Should_ReturnFalse_When_ErrorReportLines(self, *patches):
        result_mock = Mock()
        result_mock.report_lines = ['--line1--']
        result_mock.error_report_lines = ['--error-line1--']
        result = verify_result(result_mock, Mock(), Mock())
        self.assertFalse(result)

    def test__verify_result_Should_ReturnTrue_When_ReportLinesAndNoErrorReportLines(self, *patches):
        result_mock = Mock()
        result_mock.report_lines = ['--line1--', '--line2--']
        result_mock.error_report_lines = []
        result = verify_result(result_mock, Mock(), Mock())
        self.assertTrue(result)

    def test__get_complexity_Should_ReturnExpected_When_CalledNoVerbose(self, *patches):
        result_mock = Mock()
        result_mock.report_lines = [
            '\n',
            '    M 81:4 class.ma - C (14)\n',
            '    M 231:4 class.mb - A (4)\n',
            'src/main/python/package/module.py\n',
            '    C 40:0 class.mc - B (9)\n',
            '\n',
            'Average complexity: A (3.557377049180328)']
        project_mock = Mock()
        project_mock.get_property.return_value = False
        logger_mock = Mock()
        result = get_complexity(project_mock, result_mock, logger_mock)
        expected_result = {
            'average': 3.557377049180328,
            'highest': {
                'name': 'class.ma',
                'score': 14
            }
        }
        self.assertEqual(result, expected_result)
        self.assertEqual(len(logger_mock.debug.mock_calls), 0)

    def test__get_complexity_Should_ReturnExpected_When_NoMatch(self, *patches):
        result_mock = Mock()
        result_mock.report_lines = [
            '\n',
            '    M 81:4 class.ma -\n',
            '    M 231:4 class.mb -\n',
            'src/main/python/package/module.py\n',
            '    C 40:0 class.mc -\n',
            '\n',
            'Average complexity:)']
        project_mock = Mock()
        logger_mock = Mock()
        result = get_complexity(project_mock, result_mock, logger_mock)
        expected_result = {
            'average': None,
            'highest': {
                'name': None,
                'score': 0
            }
        }
        self.assertEqual(result, expected_result)

    def test__verify_complexity_Should_ReturnFalse_When_AverageIsNone(self, *patches):
        complexity = {
            'average': None,
            'highest': {
                'name': None,
                'score': 0
            }
        }
        result = verify_complexity(complexity)
        self.assertFalse(result)

    def test__verify_complexity_Should_ReturnFalse_When_HighestNameIsNone(self, *patches):
        complexity = {
            'average': 3.557377049180328,
            'highest': {
                'name': None,
                'score': 0
            }
        }
        result = verify_complexity(complexity)
        self.assertFalse(result)

    def test__verify_complexity_Should_ReturnTrue_When_ComplexityValid(self, *patches):
        complexity = {
            'average': 3.557377049180328,
            'highest': {
                'name': 'class.ma',
                'score': 14
            }
        }
        result = verify_complexity(complexity)
        self.assertTrue(result)

    def test__process_complexity_Should_NotRaiseBuildFailedExcpetion_When_NoProperties(self, *patches):
        project_mock = Mock()
        project_mock.get_property.side_effect = [None, None]
        complexity = {
            'average': 3.557377049180328,
            'highest': {
                'name': 'class.ma',
                'score': 14
            }
        }
        process_complexity(project_mock, complexity)

    def test__process_complexity_Should_NotRaiseBuildFailedExcpetion_When_NoThresholdsExceeded(self, *patches):
        project_mock = Mock()
        project_mock.get_property.side_effect = [3.6, 15]
        complexity = {
            'average': 3.557377049180328,
            'highest': {
                'name': 'class.ma',
                'score': 14
            }
        }
        process_complexity(project_mock, complexity)

    def test__process_complexity_Should_RaiseBuildFailedExcpetion_When_AverageComplexityThresholdExceeded(self, *patches):
        project_mock = Mock()
        project_mock.get_property.side_effect = [3.5, None]
        complexity = {
            'average': 3.557377049180328,
            'highest': {
                'name': 'class.ma',
                'score': 14
            }
        }
        with self.assertRaises(BuildFailedException):
            process_complexity(project_mock, complexity)

    def test__process_complexity_Should_RaiseBuildFailedExcpetion_When_AnyComplexityThresholdExceeded(self, *patches):
        project_mock = Mock()
        project_mock.get_property.side_effect = [4.0, 13]
        complexity = {
            'average': 3.557377049180328,
            'highest': {
                'name': 'class.ma',
                'score': 14
            }
        }
        with self.assertRaises(BuildFailedException):
            process_complexity(project_mock, complexity)
