from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
import json

import scraper
import random
import chat

app = Flask(__name__)

QUEIRES = ["shirt",
    "t-shirt",
    "dress shirt",
    "casual shirt",
    "formal shirt",
    "polo shirt",
    "button-up shirt",
    "striped shirt",
    "plain shirt",
    "printed shirt",
    "sleeveless shirt",
    "hoodie",
    "v-neck shirt",
    "collared shirt",]

@app.route("/init")
def init():
    return headerify(scraper.get_images_from_query(random.sample(QUEIRES, 1)[0]))

@app.route("/aistuff")
def aistuff():
    return headerify(chat.get_ai_stuff(scraper.get_image_tags(json.loads(request.args.get('links')))))

@app.route("/right")
def right():
    return headerify(scraper.get_related_images(request.args.get('title')))

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        return headerify({})
    
def headerify(response):
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
    response.headers.add('Access-Control-Allow-Headers', 'ngrok-skip-browser-warning')
    return response