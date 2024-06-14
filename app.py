from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()

from src.helpers import field
from src import User, ActivationCode, Injector


app = Flask(__name__)


@app.route("/register", methods=["POST"])
@field("email", str)
@field("password", str)
def register(email: str, password: str) -> None:
    """Register user API route"""
    # Attempt to register the user
    try:
        User.register(email, password)
    # Failed
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    # Success
    return jsonify(
        {"message": "User registered, please check your email for the activation code"}
    )


@app.route("/activate", methods=["POST"])
@field("email", str)
@field("password", str)
@field("code", str)
def activate(email: str, password: str, code: str) -> None:
    """Activate user API route"""
    # Attempt to identify user
    user = User.get_by_email(email)
    if not user:
        return jsonify({"message": "User not found"}), 404
    # Attempt to authenticate user
    try:
        user.authenticate(password)
    # Failed
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    # Success
    # Attempt to activate user account
    try:
        user.activate(code)
    # Failed
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    # Success
    return jsonify({"message": "User activated"})


if __name__ == "__main__":

    Injector.resolve("LoggingService")

    # Init the database if needed
    db_service = Injector.resolve("DatabaseService")
    db_service.register_models(User, ActivationCode)
    db_service.create_tables(drop_old=True)

    # Register all services to the event dispatcher
    dispatch_service = Injector.resolve("DispatchService")
    for dep in Injector.dependencies.values():
        dispatch_service.subscribe(dep.get())

    # Start the app loop
    app.run(debug=True)

    # Close the app
    db_service.close()
