# recallo/api/factories.py

import factory
from factory.django import DjangoModelFactory
from django.utils import timezone

from .models import ReviewSession, StudyItem


class StudyItemFactory(DjangoModelFactory):
    class Meta:
        model = StudyItem

    @factory.lazy_attribute
    def user(self):
        raise ValueError("You must provide a user")

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph", nb_sentences=4)
    cycle_start_date = factory.LazyFunction(timezone.now)


class ReviewSessionFactory(DjangoModelFactory):
    class Meta:
        model = ReviewSession

    @factory.lazy_attribute
    def user(self):
        raise ValueError("You must provide a user")

    @factory.lazy_attribute
    def study_item(self):
        raise ValueError("You must provide a study item")
    sequence_number = factory.Iterator([1, 2, 3, 4, 5])
