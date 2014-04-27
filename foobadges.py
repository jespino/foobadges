import settings
import json
import service
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    pass

@app.route("/revoked")
def revoked():
    return json.dumps(service.get_revocation_list())

@app.route("/organization")
def organization():
    return json.dumps({
        'name': settings.ISSUER_NAME,
        'image': settings.ISSUER_IMAGE_URL,
        'url': settings.ISSUER_URL,
        'email': settings.ISSUER_EMAIL,
        'revocationList': "/revoked"
    })

@app.route("/assertion/<assertion_id>")
def assertion(assertion_id):
    return json.dumps(service.get_assertion_by_id(assertion_id))

@app.route("/criterion/<criterion_slug>")
def criterion(criterion_slug):
    return json.dumps(service.get_criterion_by_slug(criterion_slug))

@app.route("/badge/<badge_slug>")
def badge(badge_slug):
    return json.dumps(service.get_badge_by_slug(badge_slug))

if __name__ == '__main__':
    app.run(debug=True)
