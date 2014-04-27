from pymongo import MongoClient
import settings
from cmd import Cmd
import sys

client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
db = client[settings.MONGO_DB]


class FooBadgesCmdClient(Cmd):
    def do_EOF(self, args):
        sys.exit()

    def do_exit(self, args):
        sys.exit()

    def do_revoke(self, args):
        assertion_id = input("Assertion id: ")
        reason = input("Reason: ")
        db.revocations.insert({assertion_id: reason})

    def do_new_badge(self, args):
        slug = input("slug: ")
        title = input("Title: ")
        description = input("Description: ")
        image = input("Image url: ")
        criteria = input("Criteria: ")

        num_of_alignments = input("Number of alignments: ")
        alignments = []
        for x in range(int(num_of_alignments)):
            alignment_name = input("Alignment %s name: " % x)
            alignment_url = input("Alignment %s url: " % x)
            alignment_description = input("Alignment %s description: " % x)
            alignments.append({
                "name": alignment_name,
                "url": alignment_url,
                "description": alignment_description,
            })

        tags = []
        num_of_tags = input("Number of tags: ")
        for x in range(int(num_of_tags)):
            tags.append(input("Tag: "))

        db.badges.insert({
            "_id": slug,
            "title": title,
            "description": description,
            "image": image,
            "criteria": criteria,
            "alignments": alignments,
            "tags": tags,
            "issuer": "/issuer"
        })

if __name__ == '__main__':
    cmd = FooBadgesCmdClient()
    cmd.cmdloop("Welcome to foo badges client")
