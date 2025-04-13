import uuid
from flask import request, jsonify

def get_or_create_user_id():
    user_id = request.cookies.get("user_id")
    if not user_id:
        user_id = str(uuid.uuid4())
    return user_id
