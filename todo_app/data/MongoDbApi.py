from todo_app.data.Status import Status
from todo_app.data.FieldNames import FieldNames
import pymongo
import os
import datetime
from bson.objectid import ObjectId


class MongoDbApi:

    MONGO_URL = 'cluster0.p7ckx.mongodb.net'

    @classmethod
    def init(cls, db_name=None):
        """Set MongoDB ENV Variables."""

        cls.MONGO_USER = os.environ.get('MONGO_USER')
        if not cls.MONGO_USER:
            raise ValueError(
                "No MONGO_USER set for MongoDB calls. Did you follow the setup instructions?")

        cls.MONGO_PASS = os.environ.get('MONGO_PASS')
        if not cls.MONGO_PASS:
            raise ValueError(
                "No MONGO_PASS set for MongoDB calls. Did you follow the setup instructions?")

        if not db_name:
            cls.MONGO_DB = os.environ.get('MONGO_DB')
        else:
            cls.MONGO_DB = db_name
        print(f'Mongo DB being set is: {cls.MONGO_DB}')
        if not cls.MONGO_DB:
            raise ValueError(
                "No MONGO_DB set for MongoDB calls. Did you follow the setup instructions?")

        cls.MONGO_CONN_STR = f'mongodb+srv://{cls.MONGO_USER}:{cls.MONGO_PASS}@{cls.MONGO_URL}/{cls.MONGO_DB}?w=majority'

        client = pymongo.MongoClient(cls.MONGO_CONN_STR)
        cls.db = client[cls.MONGO_DB]

    @classmethod
    def get_items(cls) -> list:
        return cls.db.items.find()

    @classmethod
    def get_item_by_id(cls, item_id) -> list:
        return cls.db.items.find_one({FieldNames.ID: item_id})

    @classmethod
    def add_item(cls, item_title):
        new_item = {
            FieldNames.TITLE: item_title,
            FieldNames.STATUS: Status.TODO.value,
            FieldNames.DATE_LAST_ACTIVITY: datetime.datetime.utcnow()
        }
        new_item_id = cls.db.items.insert_one(new_item).inserted_id

        return cls.get_item_by_id(new_item_id)

    @classmethod
    def delete_item(cls, item_id):
        result = cls.db.items.delete_one({FieldNames.ID: ObjectId(item_id)})
        return result

    @classmethod
    def update_item_status(cls, item_id, new_status):
        query = {FieldNames.ID: ObjectId(item_id)}
        new_values = {
            "$set": {
                FieldNames.STATUS: new_status,
                FieldNames.DATE_LAST_ACTIVITY: datetime.datetime.utcnow()
            }
        }

        number_of_updates = cls.db.items.update_one(query, new_values)
        return number_of_updates

    @classmethod
    def doing_item(cls, item_id):
        return cls.update_item_status(item_id, Status.DOING.value)

    @classmethod
    def done_item(cls, item_id):
        return cls.update_item_status(item_id, Status.DONE.value)
