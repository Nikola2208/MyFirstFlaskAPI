from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import *
from database import database
from models import ItemModel
import sqlalchemy.exc as exc
from flask_jwt_extended import jwt_required, get_jwt

blueprint = Blueprint("items", __name__, description="Item operations")


@blueprint.route("/item/<int:item_id>")
class Item(MethodView):
    @blueprint.response(200, ItemResponseSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @blueprint.arguments(schema=ItemUpdateSchema)
    @blueprint.response(200, ItemResponseSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item is None:
            abort(404, message="Item with chosen id does not exist.")
        item.name = item_data["name"]
        item.price = item_data["price"]
        item.description = item_data["description"]
        try:
            database.session.add(item)
            database.session.commit()
        except exc.IntegrityError:
            abort(400, message="Item with same name already exists.")
        return item

    def delete(self, item_id):
        item = ItemModel.query.get(item_id)
        if item is None:
            abort(404, message="Item with chosen id does not exist.")
        database.session.delete(item)
        database.session.commit()
        return {"message": "Item successfully deleted."}


@blueprint.route("/items")
class ItemList(MethodView):
    @blueprint.response(200, ItemResponseSchema(many=True))
    def get(self):
        return ItemModel.query.all()


@blueprint.route("/item")
class ItemCreation(MethodView):
    @jwt_required()
    @blueprint.arguments(schema=ItemCreateSchema)
    @blueprint.response(201, ItemResponseSchema)
    def post(self, item_data):
        if get_jwt().get("role") != 'admin':
            abort(401, message="Admin role required.")
        item = ItemModel(**item_data)
        try:
            database.session.add(item)
            database.session.commit()
        except exc.IntegrityError:
            abort(400, message="Item with same name already exists.")
        except exc.SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")
        return item

