from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.test import TestCase
from model_mommy import mommy

from goals.models import Goal, Subgoal

# Create your tests here.
User = get_user_model()


class GoalTest(TestCase):
    def setUp(self):
        self.title = "Test Goal"
        self.user = mommy.make(
            User,
            email="abc@abc.com",
            name="abc",
            password="abc"
        )

        self.end_date = datetime.now() + timedelta(days=3)

    def test_empty_title(self):
        expected_message = {'title': ['This field cannot be blank.']}
        with self.assertRaisesMessage(ValidationError, str(expected_message)):
            goal = Goal.objects.create(
                user=self.user,
                end_date=self.end_date)

    def test_empty_user(self):
        expected_message = {'user': ['This field cannot be null.']}
        with self.assertRaisesMessage(ValidationError, str(expected_message)):
            goal = Goal.objects.create(
                title=self.title,
                end_date=self.end_date)

    def test_empty_end_date(self):
        expected_message = {'end_date': ['This field cannot be null.']}
        with self.assertRaisesMessage(ValidationError, str(expected_message)):
            goal = Goal.objects.create(
                title=self.title,
                user=self.user)

    def test_user_not_model_object(self):
        user = "user"
        self.assertFalse(isinstance(user, User))
        with self.assertRaises(ValueError):
            goal = Goal.objects.create(
                title=self.title,
                user=user,
                end_date=self.end_date)

    def test_end_date_is_not_date_instance(self):
        end_date = "20121"
        self.assertFalse(isinstance(end_date, datetime))
        with self.assertRaises(ValidationError):
            goal = Goal.objects.create(
                title=self.title,
                user=self.user,
                end_date=end_date)

    def test_end_date_in_past(self):
        expected_message = 'End date should not be in past'
        end_date = datetime.now() - timedelta(days=3)
        self.assertTrue(isinstance(end_date, datetime))
        with self.assertRaisesMessage(ValidationError, expected_message):
            goal = Goal.objects.create(
                title=self.title,
                user=self.user,
                end_date=end_date)

    def test_title_should_be_less_than_100_char(self):
        title = "a" * 101
        expected_message = {'title': ['Ensure this value has at most 100 characters (it has %s).' % len(title)]}
        with self.assertRaisesMessage(ValidationError, str(expected_message)):
            goal = Goal.objects.create(
                title=title,
                user=self.user,
                end_date=self.end_date)

    def test_slug(self):
        expected_slug = slugify(self.title)
        goal = Goal.objects.create(
            title=self.title,
            user=self.user,
            end_date=self.end_date)
        self.assertEqual(goal.slug, expected_slug)


class SubgoalTest(TestCase):
    def setUp(self):
        self.title = "Goal with subgoals"
        self.user = mommy.make(
            User,
            email="abc@abc.com",
            name="abc",
            password="abc"
        )
        self.goal = mommy.make(
            Goal,
            title=self.title,
            user=self.user,
            end_date=datetime.now()
        )

    def test_subgoal_with_blank_title(self):
        expected_message = {'title': ['This field cannot be blank.']}
        with self.assertRaisesMessage(ValidationError, str(expected_message)):
            sub_goal = Subgoal.objects.create(
                title='',
                goal=self.goal)

    def test_empty_goal(self):
        expected_message = {'goal': ['This field cannot be null.']}
        with self.assertRaisesMessage(ValidationError, str(expected_message)):
            sub_goal = Subgoal.objects.create(
                title=self.title)

    def test_goal_is_not_Goal_object(self):
        goal = "user"
        self.assertFalse(isinstance(goal, Goal))
        with self.assertRaises(ValueError):
            sub_goal = Subgoal.objects.create(
                title=self.title,
                goal=goal)

    def test_end_date_is_not_date_instance(self):
        end_date = "20121"
        self.assertFalse(isinstance(end_date, datetime))
        with self.assertRaises(ValidationError):
            sub_goal = Subgoal.objects.create(
                title=self.title,
                goal=self.goal,
                end_date=end_date)

    def test_end_date_in_past(self):
        expected_message = 'End date should not be in past'
        end_date = datetime.now() - timedelta(days=3)
        self.assertTrue(isinstance(end_date, datetime))
        with self.assertRaisesMessage(ValidationError, expected_message):
            sub_goal = Subgoal.objects.create(
                title=self.title,
                goal=self.goal,
                end_date=end_date)

    def test_title_should_be_less_than_100_char(self):
        title = "a" * 101
        expected_message = {'title': ['Ensure this value has at most 100 characters (it has %s).' % len(title)]}
        with self.assertRaisesMessage(ValidationError, str(expected_message)):
            sub_goal = Subgoal.objects.create(
                title=title,
                goal=self.goal)

    def test_slug(self):
        expected_slug = slugify(self.title)
        sub_goal = Subgoal.objects.create(
            title=self.title,
            goal=self.goal)
        self.assertEqual(sub_goal.slug, expected_slug)
        self.assertEqual(sub_goal.end_date, sub_goal.goal.end_date)
        self.assertEqual(len(self.goal.subgoal_set.all()), 1)
