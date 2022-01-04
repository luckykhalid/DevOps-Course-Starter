from todo_app.data.Status import Status
from todo_app.data.FieldNames import FieldNames
import pymongo
import os
import datetime
from bson.objectid import ObjectId


class MongoDbApi:

    DEFAULT_MONGO_DB = 'devops'

    @classmethod
    def init(cls, db_name=None):
        """Set MongoDB ENV Variables."""

        cls.MONGODB_CONNECTION_STRING = os.environ.get(
            'MONGODB_CONNECTION_STRING')
        if not cls.MONGODB_CONNECTION_STRING:
            raise ValueError(
                "No MONGODB_CONNECTION_STRING set for MongoDB calls. Did you follow the setup instructions?")

        if not db_name:
            cls.MONGO_DB = cls.DEFAULT_MONGO_DB
        else:
            cls.MONGO_DB = db_name
        print(f'Mongo DB being set is: {cls.MONGO_DB}')
        if not cls.MONGO_DB:
            raise ValueError(
                "No MONGO_DB set for MongoDB calls. Error in the code, please fix!")

        client = pymongo.MongoClient(cls.MONGODB_CONNECTION_STRING)
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
