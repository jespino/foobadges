from pymongo import MongoClient
import settings

client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
db = client[settings.MONGO_DB]


def get_revocation_list():
    return list(db.revocations.find(fields={"_id": False}))

def get_assertion_by_id(assertion_id):
    return db.assertions.find_one({"_id": assertion_id})

def get_badge_by_slug(slug):
    return db.badges.find_one({"_id": slug})

def get_criterion_by_slug(slug):
    return db.criterions.find_one({"_id": slug})
