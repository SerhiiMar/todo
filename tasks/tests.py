from datetime import datetime, timezone

from django.test import TestCase

from tasks.forms import TaskForm
from tasks.models import Task, Tag


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Task.objects.create(title="task1")

    def setUp(self):
        self.task = Task.objects.first()

    def test_task_model_ordering(self):
        actual_ordering = self.task._meta.ordering
        expected_ordering = ["is_done", "-created"]
        self.assertEqual(list(actual_ordering[:2]), expected_ordering[:2])


class FormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Tag.objects.create(name="test_tag")
        test_deadline = datetime(
            2024,
            5,
            22,
            0,
            0,
        )
        cls.task_form_data = {
            "title": "test_title",
            "content": "test_content",
            "deadline": test_deadline,
            "tags": Tag.objects.all(),
        }

    def test_task_form(self):
        form = TaskForm(self.task_form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], self.task_form_data["title"])
        self.assertEqual(form.cleaned_data["content"], self.task_form_data["content"])
        expected_deadline = self.task_form_data["deadline"]
        actual_deadline = form.cleaned_data["deadline"]
        self.assertEqual(actual_deadline.year, expected_deadline.year)
        self.assertEqual(actual_deadline.month, expected_deadline.month)
        self.assertEqual(actual_deadline.day, expected_deadline.day)
        self.assertEqual(actual_deadline.hour, expected_deadline.hour)
        self.assertEqual(actual_deadline.minute, expected_deadline.minute)
        self.assertEqual(list(form.cleaned_data["tags"]), list(self.task_form_data["tags"]))
