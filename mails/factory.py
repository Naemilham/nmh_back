import factory

from .models import Email


class EmailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Email

    subject = factory.Faker("sentence", nb_words=6)
    message = factory.Faker("paragraph", nb_sentences=4)
    writer = factory.Faker("first_name")
    is_sent = factory.Faker("boolean", chance_of_getting_true=50)
    sent_at = factory.Faker("date_time")
    is_successfully_sent = factory.Faker("boolean", chance_of_getting_true=50)
    is_read = factory.Faker("boolean", chance_of_getting_true=50)
