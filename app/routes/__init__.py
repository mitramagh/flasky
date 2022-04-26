from nis import cat
from flask import Blueprint, jsonify

cat_bp = Blueprint("cat", __name__,url_prefix="/cats")

class Cat:
    def __init__(self, id, name, color, personality):
        self.id = id
        self.name = name
        self.color = color
        self.personality = personality

cats = [
    Cat(1, "Muna", "black", "mischevious"),
    Cat(2, "Matthew", "spotted", "cuddly"),
    Cat(3, "George", "Gray","Sassy")
]

# get all cats
@cat_bp.route("", methods=["GET"])
def handle_cats():
    cats_response = [vars(cat) for cat in cats]
    return jsonify(cats_response)

# get one cat
@cat_bp.route("/<cat_id>", methods=["GET"])
def get_one_cat(cat_id):
    cat_id = int (cat_id)
    chosen_cat = None
    for cat in cats:
        if cat.id == cat_id:
            chosen_cat = cat
            break

    rsp = {
        "id" : chosen_cat.id,
        "name" : chosen_cat.name,
        "color": chosen_cat.color,
        "personality": chosen_cat.personality,
    }

    return jsonify(rsp), 200