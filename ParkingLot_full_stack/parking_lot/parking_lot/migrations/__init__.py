from db_pool import operations as db_op
import os


BASE_PATH = os.path.dirname(os.path.realpath(__file__))

db_op.load_model_create_db(os.path.join(BASE_PATH, '..',
                                        'models', 'testMapData.json'))
