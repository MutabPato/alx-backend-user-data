#!/usr/bin/env python3
""" Module Session Authentication views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def view_login() -> str:
    """POST /auth_session/login
    Return:
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or email.strip() == "":
        return jsonify({"error": "email missing"}), 400
    if not password or password.strip() == "":
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]  # Assuming search returns a list of users

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    else:
        from api.v1.app import auth
        session_id = auth.create_session(user.id)

        response = jsonify(user.to_json())
        session_name = os.getenv("SESSION_NAME", "_my_session_id")
        response.set_cookie(session_name, session_id)

        return response


@app_views.route(
        '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def view_logout() -> str:
    """DELETE /auth_session/logout
    Logs out
    """
    from api.v1.app import auth
    try:
        auth.destroy_session(request)
    except Exception:
        abort(404)

    return jsonify({}), 200
