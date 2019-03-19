import os

import mongoengine as mongo

mongo_host = os.environ.get('MONGO_HOST', 'mongodb://localhost:27017/vkbot')

mongo.connect(host=mongo_host)


class User(mongo.Document):
    user_id = mongo.IntField(
        unique=True,
        required=True
    )
    first_name = mongo.StringField(null=True)
    last_name = mongo.StringField(null=True)
    username = mongo.StringField(unique=True)
    is_bot = mongo.BooleanField()
    language_code = mongo.StringField()

    context = mongo.DictField(default={})

    @staticmethod
    def create(user):
        try:
            return User.objects.get(user_id=user.id)
        except mongo.DoesNotExist:
            record = User(
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                is_bot=user.is_bot,
                language_code=user.language_code
            )
            record.save()
            return record

    @staticmethod
    def get(user):
        try:
            return User.objects.get(user_id=user.id)
        except mongo.DoesNotExist:
            return None
