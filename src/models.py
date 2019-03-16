import datetime

import mongoengine as mongo

mongo.connect('project1', host='0.0.0.0', port=27017)


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


class Queue(mongo.Document):
    type = mongo.StringField(required=True)
    user = mongo.ReferenceField(
        User,
        required=True
    )
    message = mongo.DictField(required=True)
    output = mongo.DictField(required=True)

    created = mongo.DateTimeField(default=datetime.datetime.now)
    started = mongo.DateTimeField(null=True)
    finished = mongo.DateTimeField(null=True)

    @staticmethod
    def add(**kwargs):
        record = Queue(**kwargs)
        record.save()
        return record

    @staticmethod
    def done(_id):
        try:
            task = Queue.objects.get(id=_id)
            task.update(finished=datetime.datetime.now())
            task.save()
            return True
        except mongo.DoesNotExist:
            return False

    @staticmethod
    def pop():
        query = Queue.objects(started=None, finished=None)
        if query:
            task = query[0]
            task.update(started=datetime.datetime.now())
            task.save()
            return task
        else:
            return None
