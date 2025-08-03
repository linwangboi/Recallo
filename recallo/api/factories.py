import factory
from factory.django import DjangoModelFactory

from .models import StudyItem, ReviewSession


class StudyItemFactory(DjangoModelFactory):
    class Meta:
        model = StudyItem

    @factory.lazy_attribute
    def user(self):
        raise ValueError("You must provide a user")

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph", nb_sentences=4)

class ReviewSessionFactory(DjangoModelFactory):
    class Meta:
        model = ReviewSession
    @factory.lazy_attribute
    def user(self):
        raise ValueError('You must provide a user')
    @factory.lazy_attribute
    def study_item(self):
        raise ValueError('You must provide a study item')
