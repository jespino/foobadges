import settings
import json
from flask import Flask, request, Response
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
db = client[settings.MONGO_DB]

@app.route('/')
def home():
    pass

@app.route("/revoked")
def revoked():
    cursor = db.revocations.find(fields={"_id": False})
    return Response(json.dumps(list(cursor)), content_type="application/json")

@app.route("/issuer")
def issuer():
    return Response(json.dumps({
        'name': settings.ISSUER_NAME,
        'image': settings.ISSUER_IMAGE_URL,
        'url': settings.ISSUER_URL,
        'email': settings.ISSUER_EMAIL,
        'revocationList': request.url_root + "revoked"
    }), content_type="application/json")

@app.route("/assertion/<assertion_id>")
def assertion(assertion_id):
    assertion = db.assertions.find_one({"_id": assertion_id}, fields={"_id": False})
    return Response(json.dumps(assertion), content_type="application/json")

@app.route("/badge/<badge_slug>")
def badge(badge_slug):
    badge = db.badges.find_one({"_id": badge_slug}, fields={"_id": False})
    return Response(json.dumps(badge), content_type="application/json")

if __name__ == '__main__':
    app.run(debug=True)
