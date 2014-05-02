from pymongo import MongoClient
import settings
from cmd import Cmd
import sys
from uuid import uuid4
import hashlib

from datetime import date

client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
db = client[settings.MONGO_DB]

def generate_badge_image(badge_img, assertion_uuid):
    return None

def base_url(settings):
    if ((settings.SERVER_PORT == 80 and settings.SERVER_PROTOCOL == "http")
       or (settings.SERVER_PORT == 443 and settings.SERVER_PROTOCOL == "https")):
        return "{0}://{1}{2}".format(
            settings.SERVER_PROTOCOL,
            settings.SERVER_HOST,
            settings.SERVER_BASE_PATH
        )
    else:
        return "{0}://{1}:{2}{3}".format(
            settings.SERVER_PROTOCOL,
            settings.SERVER_HOST,
            settings.SERVER_PORT,
            settings.SERVER_BASE_PATH
        )


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
            "issuer": "{}issuer".format(base_url(settings))
        })

    def do_new_assertion(self, args):
        _id = uuid4().hex

        identity_salt = uuid4().hex[:5]
        identity_type = "email"
        identity_hashed = True
        email = input("Email: ")
        identity_hash = 'sha256$' + hashlib.sha256((email + identity_salt).encode('utf-8')).hexdigest()

        evidence = input("Url with evidence of the work (or blank): ")
        expires = input("Expiration date YYYY-MM-DD format (or blank): ")

        print("Badges")
        print("------")
        for badge in db.badges.find():
            print("  - {}".format(badge['_id']))

        badge_slug = input("Slug: ")
        badge_url = "{}badge/{}".format(base_url(settings), badge_slug)
        badge_img = "{}badge_image/{}.png".format(base_url(settings), badge_slug)

        assertion_url = "{}assertion/{}".format(base_url(settings), _id)

        data = {
            "_id": _id,
            "uid": _id,
            "recipient": {
                "identity": identity_hash,
                "type": identity_type,
                "hashed": identity_hashed,
                "salt": identity_salt,
            },
            "badge": badge_url,
            "verify": {
                "type": "hosted",
                "url": assertion_url,
            },
            "issuedOn": date.today().isoformat(),
            "image": generate_badge_image(badge_img, _id)
        }

        if expires:
            data['expires'] = expires

        if evidence:
            data["evidence"] = evidence

        db.assertions.insert(data)
        print("Created assertion:", assertion_url)

if __name__ == '__main__':
    cmd = FooBadgesCmdClient()
    cmd.cmdloop("Welcome to foo badges client")
