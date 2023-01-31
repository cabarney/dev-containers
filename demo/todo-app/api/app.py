from db import TodoRepository
from flask import Flask, request
import json 

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

db = TodoRepository()

@app.route("/todos")
def get_all():
    return db.get_all(), 200

@app.route("/todos/<int:todo_id>")
def get(todo_id):
    return db.get(todo_id), 200

@app.route("/todos", methods=["POST"])
def create():
    todo = request.json
    db.create(todo)
    return "Success", 200

@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update(todo_id):
    todo = request.json
    db.update(todo_id, todo)
    return "Success", 200

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete(todo_id):
    db.delete(todo_id)
    return "Success", 200

@app.route("/hello")
def hello():
    return { "message": "Hello!!" }