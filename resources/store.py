from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import *
from database import database
from models import StoreModel
import sqlalchemy.exc as exc

blueprint = Blueprint("stores", __name__, description="Store operations")


@blueprint.route("/store/<int:store_id>")
class Store(MethodView):
    @blueprint.response(200, StoreResponseSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    @blueprint.arguments(schema=StoreUpdateSchema)
    @blueprint.response(200, StoreResponseSchema)
    def put(self, store_data, store_id):
        store = StoreModel.query.get(store_id)
        if store is None:
            abort(404, message="Store with chosen id does not exist.")
        store.name = store_data["name"]
        try:
            database.session.add(store)
            database.session.commit()
        except exc.IntegrityError:
            abort(400, message="Store with same name already exists.")
        return store

    def delete(self, store_id):
        store = StoreModel.query.get(store_id)
        if store is None:
            abort(404, message="Store with chosen id does not exist.")
        database.session.delete(store)
        database.session.commit()
        return {"message": "Store successfully deleted."}


@blueprint.route("/stores")
class StoreList(MethodView):
    @blueprint.response(200, StoreResponseSchema(many=True))
    def get(self):
        return StoreModel.query.all()


@blueprint.route("/store")
class StoreCreation(MethodView):
    @blueprint.arguments(schema=StoreCreateSchema)
    @blueprint.response(201, StoreResponseSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            database.session.add(store)
            database.session.commit()
        except exc.IntegrityError:
            abort(400, message="Store with same name already exists.")
        except exc.SQLAlchemyError:
            abort(500, message="An error occurred while inserting the store.")
        return store
