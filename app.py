import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask_pymongo import PyMongo
from flask import Flask, request, Response
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_restplus import Api
from flask_jwt import JWT
from Settings.security import authenticate, identity
from bson.json_util import dumps


# '''
# TO-DO :

# 1. CRUD methods for Users, Mealplan,Recipe and Feedbacks as in the MongoDB.
# 2. create JWT tokens or API tokens

# '''


app = Flask(__name__)
api = Api(app,
          default="Collections",
          title="Hello fresh weekly meal planner.",
          description="a Flask-pymongo data service that allows a client to \
                    read and store some publicly available Hello fresh recipes\
                     and meal plan, and allow the consumers to access the data\
                    through a REST API")
app.secret_key = "secretkey"
jwt = JWT(app, authenticate, identity)
try:
    app.config['MONGO_URI'] = "mongodb+srv://Hellofresh_user:Hellofresh123@cluster0.giqdc.mongodb.net/HelloFresh"
    mongo = PyMongo(app)
    db = mongo.db
except Exception as e:
    print(e, "cannot connect to the database")

#########################
# USERS - CRUD
#########################


@app.route('/users', methods=['GET', 'POST'])
def users():
    try:
        if request.method == 'GET':
            data = list(db.Users.find())
            print(data)
            for user in data:
                user["_id"] = str(user["_id"])
            return Response(
                response=dumps(data, default=str),
                status=200,
                mimetype="application/json"
            )
        if request.method == 'POST':
            _json = request.get_json
            result = db.Users.insert_one(_json)
            return Response(response=dumps({"message": "user created", "id": f"{result.inserted_id}"}, default=str), status=200, mimetype="application/json")
    except Exception as e:
        print(e)
        return Response(
            response=dumps(
                {"message": "can't get the user"}, default=str),
            status=404,
            mimetype="application/json"
        )


@ app.route("/users/<string:name>", methods=['PUT'])
# @jwt_required()
def update(name):
    try:
        filter = {'name': name}
        newvalues = {"$set": {'name': request.form["name"],'email': request.form["email"],'mealplanid': request.form["mealplanid"], 'feedbackid': request.form["feedbackid"]}}
        dbResponse = db.Users.update_many(filter, newvalues)
        if dbResponse.modified_count == 1:
            return Response(
                response=dumps({"message": "updated!!"}, default=str),
                status=200,
                mimetype="application/json"
            )
        return Response(
            response=dumps(
                {"message": "Nothing to Update!!"}, default=str),
            status=200,
            mimetype="application/json"
        )
    except Exception as e:
        print(e)
        return Response(
            response=dumps(
                {"message": "OOPS!! can't update"}, default=str),
            status=500,
            mimetype="application/json"
        )


@ app.route("/users/<string:name>", methods=["DELETE"])
# @jwt_required()
def delete(name):
    try:
        dbResponse=db.Users.delete_one({"name": name})
        if dbResponse.deleted_count == 1:
            return Response(
                response=dumps(
                    {"message": "Deleted!!", "name": f"{name}"}, default=str),
                status=200,
                mimetype="application/json"
            )

        return Response(
            response=dumps(
                {"message": f" username '{name}' Not Found!!"}, default=str),
            status=404,
            mimetype="application/json"
        )
    except Exception as e:
        print(e)
        return Response(
            response=dumps(
                {"message": "OOPS!! can't delete"}, default=str),
            status=500,
            mimetype="application/json"
        )

#########################
# MEAL_PLAN - CRUD
#########################


@ app.route('/Mealplan', methods=['GET', 'POST'])
# @jwt_required()
def mealPlan():
    try:
        if request.method == 'GET':
            data=list(db.Meal_Plan.find())
            print(data)
            for plan in data:
                plan["_id"]=str(plan["_id"])
            return Response(
                response=dumps(data, default=str),
                status=200,
                mimetype="application/json"
            )
        if request.method == 'POST':
            _json=request.get_json()
            result=db.Meal_Plan.insert_one(_json)
            return Response(
                response=dumps({"message": "Meal Plan added!", "id": f"{result.inserted_id}"
                                }, default=str),
                status=200,
                mimetype="application/json"
            )
    except Exception as e:
        print(e)
        return Response(
            response=dumps(
                {"message": "can't get the Plan"}, default=str),
            status=404,
            mimetype="application/json"
        )


@ app.route("/Mealplan/<string:preference>", methods=['PUT'])
# @jwt_required()
def update_meal(preference):
    try:
        filter={'preference': preference}
        newvalues={"$set": {"recipe_id": request.form["recipe_id"],
                              "preference": request.form["preference"],
                              "people": request.form["people"],
                              "feedback": request.form["feedback"]}}
        dbResponse=db.Meal_Plan.update_many(filter, newvalues)
        if dbResponse.modified_count == 1:
            return Response(
                response=dumps({"message": "updated!!"}, default=str),
                status=200,
                mimetype="application/json"
            )
        return Response(
            response=dumps(
                {"message": "Nothing to Update!!"}, default=str),
            status=200,
            mimetype="application/json"
        )
    except Exception as e:
        print(e)
        return Response(
            response=dumps(
                {"message": "OOPS!! can't update"}, default=str),
            status=500,
            mimetype="application/json"
        )


@ app.route("/Mealplan/<string:preference>", methods=["DELETE"])
# @jwt_required()
def delete_plan(preference):
    try:
        dbResponse=db.Meal_Plan.delete_one({"preference": preference})
        if dbResponse.deleted_count == 1:
            return Response(
                response=dumps(
                    {"message": "Deleted!!", "preference": f"{preference}"}, default=str),
                status=200,
                mimetype="application/json"
            )

        return Response(
            response=dumps(
                {"message": f" Meal Plan '{preference}' Not Found!!"},  default=str),
            status=404,
            mimetype="application/json"
        )
    except Exception as e:
        print(e)
        return Response(
            response=dumps(
                {"message": "OOPS!! can't delete"}, default=str),
            status=500,
            mimetype="application/json"
        )

#########################
# RECIPES - CRUD
#########################


@ app.route('/Recipes', methods=['GET', 'POST'])
def meal():
    try:
        if request.method == 'GET':
            data=list(db.Recipes.find())
            print(data)
            for meal in data:
                meal["_id"]=str(meal["_id"])
            return Response(
                response=dumps(data, default=str),
                status=200,
                mimetype="application/json"
            )
        if request.method == 'POST':
            _json=request.get_json()
            result=db.Recipes.insert_one(_json)
            # resp = jsonify('Result json %s ' % result.inserted_id)

            return Response(
                response=dumps({"message": "Recipe is added!", "id": f"{result.inserted_id}"
                                }, default=str),
                status=200,
                mimetype="application/json"
            )
    except Exception as e:
        print(e)
        return Response(
            response=dumps(
                {"message": "can't get the Recipe"}, default=str),
            status=404,
            mimetype="application/json"
        )


@ app.route("/Recipes/<string:title>", methods=['PUT'])
# @jwt_required()
def update_recipe(title):
    try:
        filter={'title': title}
        newvalues={"$set": {"instructions": request.form["instructions"],
                              "ingredients": request.form["ingredients"],
                              "title": request.form["title"],
                              "feedbacks": request.form["feedbacks"],
                              "mealplanid": request.form["mealplanid"]}}
        dbResponse=db.Recipes.update_many(filter, newvalues)
        if dbResponse.modified_count == 1:
            return Response(
                response=dumps({"message": "updated!!"}, default=str),
                status=200,
                mimetype="application/json"
            )
        return Response(
            response=dumps(
                {"message": "Nothing to Update!!"}, default=str),
            status=200,
            mimetype="application/json"
        )
    except Exception as e:
        print(e)
        return Response(
            response=dumps(
                {"message": "OOPS!! can't update"}, default=str),
            status=500,
            mimetype="application/json"
        )


@ app.route("/Recipes/<string:title>", methods=["DELETE"])
# @jwt_required()
def delete_recipe(title):
    try:
        dbResponse=db.Meal_Plan.delete_one({"title": title})
        print("delete record", dbResponse.raw_result)
        if dbResponse.deleted_count == 1:
            return Response(
                response=dumps(
                    {"message": "Deleted!!", "title": f"{title}"}, default=str),
                status=200,
                mimetype="application/json"
            )

        return Response(
            response=dumps(
                {"message": f" Recipe '{title}' cannot be deleted without deleting parent Meal plan"}, default=str),
            status=412,
            mimetype="application/json"
        )
    except Exception as e:
        print(e)
        return Response(
            response=dumps(
                {"message": "OOPS!! can't delete"}, default=str),
            status=500,
            mimetype="application/json"
        )

#########################
# FEEDBACK - CRUD
#########################


@ app.route('/Feedbacks', methods=['GET', 'POST'])
def feedback():
    try:
        if request.method == 'GET':
            data=list(db.Feedbacks.find())
            print(data)
            for feedback in data:
                feedback["_id"]=str(feedback["_id"])
            return Response(
                response=dumps(data, default=str),
                status=200,
                mimetype="application/json"
            )
        if request.method == 'POST':
            _json=request.get_json()
            result=db.Feedbacks.insert_one(_json)
            return Response(
                response=dumps({"message": "Feedbacks is added!", "id": f"{result.inserted_id}"
                                }, default=str),
                status=200,
                mimetype="application/json"
            )
    except Exception as e:
        print(e)
        return Response(
            response=dumps(
                {"message": "can't get the Feedbacks,check if the Id is unique"}, default=str),
            status=404,
            mimetype="application/json"
        )


# @app.route("/Feedbacks/<string:username>", methods=['PUT'])
# # @jwt_required()
# def update_feedback(username):
#     try:
#         filter = {'username': username}
#         newvalues = {"$set": {"mealplanid": request.form["mealplanid"],
#                               "recipeid": request.form["recipeid"],
#                               "username": request.form["username"],
#                               "userid": request.form["userid"],
#                               "feedback": request.form["feedback"],
#                               }}
#         dbResponse = db.Feedbacks.update_many(filter, newvalues)
#         if dbResponse.modified_count == 1:
#             return Response(
#                 response=dumps({"message": "updated!!"}, default=str),
#                 status=200,
#                 mimetype="application/json"
#             )
#         return Response(
#             response=dumps(
#                 {"message": "Nothing to Update!!"}, default=str),
#             status=200,
#             mimetype="application/json"
#         )
#     except Exception as e:
#         print(e)
#         return Response(
#             response=dumps(
#                 {"message": "OOPS!! can't update"}, default=str),
#             status=500,
#             mimetype="application/json"
#         )


# @app.route("/Feedbacks/<string:title>", methods=["DELETE"])
# # @jwt_required()
# def delete_feedbacks(title):
#     try:
#         dbResponse = db.Feedbacks.delete_one({"title": title})
#         if dbResponse.deleted_count == 1:
#             return Response(
#                 response=dumps(
#                     {"message": "Deleted!!", "title": f"{title}"}, default=str),
#                 status=200,
#                 mimetype="application/json"
#             )

#         return Response(
#             response=dumps(
#                 {"message": "Not Found!!", "title": f"{title}"}, default=str),
#             status=404,
#             mimetype="application/json"
#         )
#     except Exception as e:
#         print(e)
#         return Response(
#             response=dumps(
#                 {"message": "OOPS!! can't delete"}, default=str),
#             status=500,
#             mimetype="application/json"
#         )


if __name__ == "__main__":
    app.run(debug=True)
