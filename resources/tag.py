from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import *
from database import database
from models import TagModel, StoreModel, ItemModel
import sqlalchemy.exc as exc

blueprint = Blueprint("tags", __name__, description="Tag operations")


@blueprint.route("/store/<int:store_id>/tags")
class TagListForStore(MethodView):
    @blueprint.response(200, TagResponseSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()


@blueprint.route("/tag")
class TagCreation(MethodView):
    @blueprint.arguments(schema=TagCreateSchema)
    @blueprint.response(201, TagResponseSchema)
    def post(self, tag_data):
        tag = TagModel(**tag_data)
        StoreModel.query.get_or_404(tag.store_id)
        try:
            database.session.add(tag)
            database.session.commit()
        except exc.IntegrityError:
            abort(400, message="Tag with same name already exists.")
        except exc.SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")
        return tag


@blueprint.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blueprint.response(200, TagResponseSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        if tag is None:
            abort(404, message="Tag with chosen id does not exist.")
        if not tag.items:
            database.session.delete(tag)
            database.session.commit()
            return {"message": "Tag successfully deleted."}
        abort(400, message="Tag contains items.")


@blueprint.route("/item/<int:item_id>/tag/<int:tag_id>")
class ItemTagBinding(MethodView):
    @blueprint.response(201, TagResponseSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        if item.store_id == tag.store_id:
            tag.items.append(item)
        else:
            abort(400, message="Tag and item do not have same store id.")
        try:
            database.session.add(tag)
            database.session.commit()
        except exc.SQLAlchemyError:
            abort(500, message="An error occurred.")
        return tag


@blueprint.route("/item/<int:item_id>/tag/<int:tag_id>")
class ItemTagUnbinding(MethodView):
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        tag.items.remove(item)
        try:
            database.session.add(tag)
            database.session.commit()
        except exc.SQLAlchemyError:
            abort(500, message="An error occurred.")
        return {"message": "Item is removed from tag successfully."}
