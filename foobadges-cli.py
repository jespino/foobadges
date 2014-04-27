from pymongo import MongoClient
import settings
from cmd import Cmd

client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
db = client[settings.MONGO_DB]


class FooBadgesCmdClient(Cmd):
    def do_revoke(self, args):
        print(args)
        assertion_id = input("Assertion id: ")
        reason = input("Reason: ")
        db.revocations.insert({assertion_id: reason})

if __name__ == '__main__':
    cmd = FooBadgesCmdClient()
    cmd.cmdloop("Welcome to foo badges client")
