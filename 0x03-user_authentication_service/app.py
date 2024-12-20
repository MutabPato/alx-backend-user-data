#!/usr/bin/env python3
"""
Basic Flask app
"""


from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def index() -> None:
    """
    Returns a welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users() -> None:
    """
    Registers a user
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200

    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """
    Logs a user in
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        if session_id:
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", session_id)
            return response
        else:
            return jsonify({"message": "Failed to create session"}), 500
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout():
    """
    Logs a user out
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('index'))
    else:
        abort(403)


@app.route("/profile", methods=["GET"])
def profile():
    """
    Profile function
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user:
        return jsonify({"email": user.email}), 200

    else:
        abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password():
    """
    Get reset password token
    """
    email = request.form.get("email")

    if not email:
        return jsonify({"message": "Email is required"}), 403

    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token})
    except ValueError:
        return jsonify({"message": "Email not found"}), 403


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """
    Updates password end-point
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    if not reset_token or not new_password:
        return jsonify(
                {"message": "Reset token and new password are required"}), 400

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        return jsonify({"message": "Invalid token"}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", threaded=False)
