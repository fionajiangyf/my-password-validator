import flask


# TODO: change this to your academic email
AUTHOR = "fionaj@seas.upenn.edu"


app = flask.Flask(__name__)


# This is a simple route to test your server


@app.route("/")
def hello():
    return f"Hello from my Password Validator! &mdash; <tt>{AUTHOR}</tt>"


# This is a sample "password validator" endpoint
# It is not yet implemented, and will return HTTP 501 in all situations


@app.route("/v1/checkPassword", methods=["POST"])
def check_password():
    data = flask.request.get_json() or {}
    pw = data.get("password", "")

    # FIXME: to be implemented
    if len(pw) < 8:
        return flask.jsonify({"valid": False, "reason": "Password must be at least 8 characters long."}), 200
    if not any(c.isupper() for c in pw):
        return flask.jsonify({"valid": False, "reason": "Password must contain at least one uppercase letter."}), 200
    if not any(c.isdigit() for c in pw):
        return flask.jsonify({"valid": False, "reason": "Password must contain at least one digit."}), 200
    if not any(c in "!@#$%^&*" for c in pw):
        return flask.jsonify({"valid": False, "reason": "Password must contain at least one special character (!@#$%^&*)."}), 200

    return flask.jsonify({"valid": True, "reason": "Valid Password"}), 200
