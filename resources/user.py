from flask.views import MethodView
from flask_smorest import Blueprint, abort
from blocklist import BLOCKLIST
from schemas import *
from database import database
from models import UserModel, UserRole
import sqlalchemy.exc as exc
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

blueprint = Blueprint("users", __name__, description="User operations")


@blueprint.route("/user/<int:user_id>")
class Store(MethodView):
    @blueprint.response(200, UserResponseSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        if user is None:
            abort(404, message="User with chosen id does not exist.")
        database.session.delete(user)
        database.session.commit()
        return {"message": "User successfully deleted."}


@blueprint.route("/register")
class UserRegistration(MethodView):
    @blueprint.arguments(schema=UserRegistrationSchema)
    @blueprint.response(201, UserResponseSchema)
    def post(self, user_data):
        user = UserModel(**user_data)
        user.password = pbkdf2_sha256.hash(user.password)
        roles = []
        for role in UserRole:
            roles.append(role.value)
        if user.role.lower() in roles:
            user.role = user.role.lower()
        else:
            abort(400, message="Role does not exist.")
        try:
            database.session.add(user)
            database.session.commit()
        except exc.IntegrityError:
            abort(400, message="User with same username already exists.")
        except exc.SQLAlchemyError:
            abort(500, message="An error occurred while inserting the user.")
        return user


@blueprint.route("/login")
class UserLogin(MethodView):
    @blueprint.arguments(schema=UserLoginSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            token = create_access_token(identity=user.id, additional_claims={'role':user.role})
            return {"token": token}
        abort(401, message="Invalid credentials.")


@blueprint.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "User successfully logged out."}
