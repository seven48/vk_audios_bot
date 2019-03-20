import os
import re

import mongoengine as mongo

from src.utils import logger

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


class Track(mongo.Document):
    owner_id = mongo.StringField(null=False)
    data_id = mongo.StringField(null=False)
    title = mongo.StringField(null=False)
    artist = mongo.StringField(null=False)
    telegram_id = mongo.StringField(null=True)

    @staticmethod
    def create(track):
        owner_id, data_id = track.get('data-id').split('_')[:2]
        try:
            return Track.objects.get(
                owner_id=owner_id,
                data_id=data_id
            )
        except mongo.DoesNotExist:
            logger.info(f'Track new {owner_id}_{data_id}')
            record = Track(
                owner_id=owner_id,
                data_id=data_id,
                title=track.get('title'),
                artist=track.get('artist')
            )
            record.save()
            return record


class Artist(mongo.Document):
    name = mongo.StringField(null=False)
    link = mongo.StringField(null=False)

    @staticmethod
    def create(artist):
        link = artist.get('link').split('/')[-1]
        try:
            return Artist.objects.get(
                link=link
            )
        except mongo.DoesNotExist:
            logger.info(f'Artist new {link}')
            record = Artist(
                name=artist.get('name'),
                link=link
            )
            record.save()
            return record


class Playlist(mongo.Document):
    owner_id = mongo.StringField(null=False)
    data_id = mongo.StringField(null=False)
    access_hash = mongo.StringField(null=False)
    title = mongo.StringField(null=False)
    subtitle = mongo.StringField(null=True)

    @staticmethod
    def create(playlist):
        pattern = r"^\/.*playlist-(\d+)_(\d+).*access_hash=(\w+).*$"
        regexp = re.match(pattern, playlist.get('link'))
        owner_id = regexp.group(1)
        data_id = regexp.group(2)
        access_hash = regexp.group(3)
        try:
            return Playlist.objects.get(
                owner_id=owner_id,
                data_id=data_id
            )
        except mongo.DoesNotExist:
            logger.info(f'Playlist new {owner_id}_{data_id}')
            record = Playlist(
                owner_id=owner_id,
                data_id=data_id,
                access_hash=access_hash,
                title=playlist.get("title"),
                subtitle=playlist.get('subtitle')
            )
            record.save()
            return record
