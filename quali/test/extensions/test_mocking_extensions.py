from unittest import TestCase
from mock import Mock
from quali.testing.extensions import mocking_extensions


class TestMockingExtensions (TestCase):

    class StubbedClass:

        def say (self, who, what, connector, target ):
            pass

        def say_with_default(self, who, what, connector, target="true"):
            pass

    def setUp(self):
        mocking_extensions.bootstrap()

    def test_throws_error_if_expected_arg_was_not_provided(self):
        mock_obj = Mock()

        #Another variation, was not provided but has a default value
        mock_obj.say_with_default(who="my", what="name", connector="is")

        self.assertRaisesRegexp(AssertionError, "target", mock_obj.say_with_default.smarter_assert_called_once_with,
                                TestMockingExtensions.StubbedClass.say, who="my", target="dog")


    def test_throws_error_if_expected_arg_was_different_than_recorded_one(self):
        mock_obj = Mock()

        mock_obj.say(who="my", what="name", connector="is", target="bill")

        self.assertRaisesRegexp(AssertionError, "my" ,mock_obj.say.smarter_assert_called_once_with, TestMockingExtensions.StubbedClass.say, who="yours", target="dog")


    def test_throws_error_if_call_to_mock_was_illegal_missing_arguments_with_no_defaults(self):

        mock_obj = Mock()

        mock_obj.say("my", "name", "is")

        self.assertRaisesRegexp(AssertionError, "target", mock_obj.say.smarter_assert_called_once_with, TestMockingExtensions.StubbedClass.say, who="my", connector="is")


    def test_validates_specific_named_arguments_without_specifying_all_arguments(self):
        mock_obj = Mock()

        mock_obj.say(who="my", what="name", connector="is", target="dog")

        mock_obj.say.smarter_assert_called_once_with(TestMockingExtensions.StubbedClass.say, who="my", target="dog")


