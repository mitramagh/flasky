from flask import Blueprint, jsonify, request, make_response, abort
from app.models.humans import Human 
from app.models.cats import Cat
from app import db 

humans_bp = Blueprint("humans", __name__,url_prefix="/humans")

@humans_bp.route('', methods=['POST'])
def create_human():
    request_body = request.get_json()
    new_human = Human(name = request_body["name"])

    db.session.add(new_human)
    db.session.commit()

    return {
       "msg": f"Successfully Create {new_human.name} with {new_human.id}"
    }, 201


@humans_bp.route('', methods=['GET'])
def get_all_human():
    
    humans = Human.query.all()

    rsp = []
    for human in humans:
        rsp.append(
            {
                "id": human.id,
                "name": human.name
            }
        )

    return jsonify(rsp), 200


def validate_human(human_id):
    try:
        human_id=int(human_id)

    except:
        abort(make_response({'msg': f"Invalid id {human.id}"}, 400))

    human = Human.query.get(human_id)

    if not human:
        abort(make_response({'msg': f"No human with id {human.id}"}, 404))

    return human



    
@humans_bp.route('/<human_id>/cats', methods=['POST'])
def create_cat(human_id):
    human = validate_human(human_id)
    request_body=request.get_json()

    new_cat = Cat(
        name= request_body["name"],
        color=request_body["color"],
        age=request_body["age"],
        human = human
        )

    db.session.add(new_cat)
    db.session.commit()

    return {
        "msg": f" New cat {new_cat.name} created for {human.name}"
    }, 201


@humans_bp.route('/<human_id>/cats', methods=['GET'])
def get_cats(human_id):
    human = validate_human(human_id)
    
    rsp =[]
    for cat in human.cats:
        rsp.append(
            {
                "id":cat.id,
                "name": cat.name,
                "color": cat.color,
                "age": cat.age
            }
        )

    return jsonify(rsp), 200
