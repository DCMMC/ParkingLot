from django.core.management.base import BaseCommand
import os
from db_pool import operations as db_op


BASE_PATH = os.path.dirname(os.path.realpath(__file__))


def create_db():
    db_op.load_model_create_db(os.path.join(
        BASE_PATH, '..', '..', '..', 'models',
        'testMapData.json'))


class Command(BaseCommand):
    def handle(self, **options):
        create_db()
