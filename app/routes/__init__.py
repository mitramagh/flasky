from nis import cat
from flask import Blueprint, jsonify, request, make_response, abort
from app.models.cats import Cat 
from app import db 

cats_bp = Blueprint("cat", __name__,url_prefix="/cats")

@cats_bp.route('', methods=['POST'])
def create_one_cat():
    request_body = request.get_json()
    new_cat = Cat(name=request_body["name"],
                  age=request_body["age"],
                  color=request_body["color"])

    db.session.add(new_cat)
    db.session.commit()

    return {
        "id":new_cat.id,
        "msg": "successfully created cat with id" }, 201

@cats_bp.route('', methods=['GET'])
def get_all_cats():
    params = request.args
    if "color" in params and "age" in params:
        color_name = params["color"]
        age_value=params["age"]
        cats = Cat.query.filter_by(color = color_name, age = age_value)
    elif "color" in params:
        color_name = params["color"]
        cats = Cat.query.filter_by(color = color_name)
    elif "age" in params:
        age_value=params["age"]
        cats = Cat.query.filter_by(age = age_value)
    else:
        cats= Cat.query.all()


    cat_response = []
    for cat in cats:
        cat_response.append({
            'id':cat.id,
            'name':cat.name,
            'age':cat.age,
            'color':cat.color
        })
    return jsonify(cat_response)

# class Cat:
#     def __init__(self, id, name, color, personality):
#         self.id = id
#         self.name = name
#         self.color = color
#         self.personality = personality

# cats = [
#     Cat(1, "Muna", "black", "mischevious"),
#     Cat(2, "Matthew", "spotted", "cuddly"),
#     Cat(3, "George", "Gray","Sassy")
# ]

# get all cats
# @cat_bp.route("", methods=["GET"])
# def handle_cats():
#     cats_response = [vars(cat) for cat in cats]
#     return jsonify(cats_response)

def get_cat_or_abort(cat_id):
    try:
        cat_id = int (cat_id)
    except ValueError:
        rsp =  {"msg": f"Invalid id:{cat_id}"}
        abort( make_response (jsonify(rsp), 400))
        
    chosen_cat = Cat.query.get(cat_id)

    if chosen_cat is None:
        abort( make_response({"massage": f" cat {cat_id} not found"}, 404))
    
    return chosen_cat




# get one cat
@cats_bp.route("/<cat_id>", methods=["GET"])
def get_one_cat(cat_id):
    # try:
    #     cat_id = int (cat_id)
    # except ValueError:
    #     rsp =  {"msg": f"Invalid id:{cat_id}"}
    #     return jsonify(rsp), 400
    chosen_cat = get_cat_or_abort(cat_id)

    #     for cat in cats:
    #         if cat.id == cat_id:
    #             chosen_cat = cat
    #             break
    # if chosen_cat is None:
    #     return {"massage": f" cat {cat_id} not found"}, 404

    request_body = request.get_json()

    rsp = {
        "id" : chosen_cat.id,
        "name" : chosen_cat.name,
        "color": chosen_cat.color,
        "age": chosen_cat.age
    }

    return jsonify(rsp), 200


    # update chosen cat
@cats_bp.route("/<cat_id>", methods=["PUT"])
def update_one_cat(cat_id):
    # try:
    #     cat_id = int (cat_id)
    # except ValueError:
    #     rsp =  {"msg": f"Invalid id:{cat_id}"}
    #     return jsonify(rsp), 400
    chosen_cat = get_cat_or_abort(cat_id)

    #     for cat in cats:
    #         if cat.id == cat_id:
    #             chosen_cat = cat
    #             break
    # if chosen_cat is None:
    #     return {"massage": f" cat {cat_id} not found"}, 404

    request_body = request.get_json()
    try:
        chosen_cat.name = request_body["name"]
        chosen_cat.age = request_body["age"]
        chosen_cat.color = request_body["color"]
    except KeyError:
        return {
            "msg": "name, age, and color are required"
        }

    db.session.commit()

    return make_response(f"Cat #{chosen_cat.id} successfully updated"), 200

    # delete chosen cat
@cats_bp.route("/<cat_id>", methods=["DELETE"])
def delete_one_cat(cat_id):
    # try:
    #     cat_id = int (cat_id)
    # except ValueError:
    #     rsp =  {"msg": f"Invalid id:{cat_id}"}
    #     return jsonify(rsp), 400

    chosen_cat = get_cat_or_abort(cat_id)
    # if chosen_cat is None:
    #     rsp =  {"massage": f" cat {cat_id} not found"}
    #     return jsonify(rsp), 404

    db.session.delete(chosen_cat)
    db.session.commit()

    return { 
        "msg": f"Cat # {chosen_cat.id} successfully deleted"
    }