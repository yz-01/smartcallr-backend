import factory
from django.contrib.auth.models import User
from datetime import datetime
from faker import Faker
from leads.models import Lead
from calls.models import Call

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_staff = False


class AdminUserFactory(UserFactory):
    is_staff = True
    is_superuser = True


class LeadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lead

    name = factory.Faker('name')
    phone = factory.Faker('phone_number')
    email = factory.Faker('email')
    created_by = factory.SubFactory(UserFactory)


class CallFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Call

    lead = factory.SubFactory(LeadFactory)
    phone_number = factory.Faker('phone_number')
    start_time = factory.Faker('date_time_this_year')
    end_time = factory.LazyAttribute(lambda obj: fake.date_time_between_dates(
        datetime_start=obj.start_time,
        datetime_end=obj.start_time.replace(hour=23, minute=59, second=59)
    ))
    status = factory.Iterator(['completed', 'failed', 'busy', 'no-answer'])
    transcription = factory.Faker('text', max_nb_chars=500)
    summary = factory.Faker('text', max_nb_chars=200)
    notes = factory.Faker('text', max_nb_chars=300)
    recording_url = factory.Faker('url')
    twilio_call_sid = factory.Faker('uuid4')
