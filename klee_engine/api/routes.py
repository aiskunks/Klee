from flask import send_from_directory, Response, request
from flask_login import login_user, login_required, current_user
from klee_engine import modules, models
from klee_engine.models import users
from klee_engine.application import backend_application
from klee_engine.application.settings import BackendSettings
from klee_engine.api import schemas, route_utils
from klee_engine.api.db_constraint_handlers import (
    experiment_module,
    experiment_module_fk,
    user_email_key,
    wrong_password,
    wrong_email
)


#########################
#  Experiment API view  #
#########################

@backend_application.route("/modules", methods=["GET"])
def get_module_list():
    return {"modules": list(modules.MODULES.keys())}


@backend_application.route("/experiment/list", methods=["GET", "POST"])
@login_required
@route_utils.serialize_response_list(
    schema_out=schemas.ExperimentOutList,
    list_kwarg="experiments"
)
def get_experiments():
    print(request.json)
    print("IAMHERE")
    # print(name)
    print(request.data)
    print(request.files)
    return models.Experiment.query.filter_by(user_id=current_user.id)


@backend_application.route("/experiment/<experiment_id>", methods=["GET"])
@login_required
@route_utils.serialize_response(schema_out=schemas.ExperimentOut)
def get_experiment_by_id(experiment_id):
    return models.Experiment.query.get(experiment_id)


@backend_application.route("/experiment/new", methods=["GET", "POST"])
@login_required
@route_utils.validate_post(schema_in=schemas.ExperimentIn)
@route_utils.serialize_response(schema_out=schemas.ExperimentOut)
def create_experiment_api(name, experiment_nodes):
    dataset_file = request.files["dataset"]
    return models.create_experiment(name=name, user=current_user, dataset_file=dataset_file)


@backend_application.route(
    rule="/experiment/<experiment_id>/node/create",
    methods=["POST"]
)
@login_required
@route_utils.validate_post(
    schema_in=schemas.ExperimentNodeIn,
    db_handlers=[experiment_module, experiment_module_fk]
)
@route_utils.serialize_response(schema_out=schemas.ExperimentNodeOut)
def create_node(module_name, input_from, experiment_id):
    return models.create_experiment_node(
        module_name=module_name,
        input_from=input_from,
        experiment_id=experiment_id
    )


#####################
#  USER AUTH VIEWS  #
#####################

@backend_application.route("/user/sign-up", methods=["POST"])
@route_utils.validate_post(schema_in=schemas.SignUp, db_handlers=[user_email_key])
@route_utils.serialize_response(schema_out=schemas.SignUpOut)
def sign_up(email, password):
    return models.create_user(email=email, password=password)


@backend_application.route("/user/sign-in", methods=["POST"])
@route_utils.validate_post(schema_in=schemas.SignUp, db_handlers=[wrong_email, wrong_password])
@route_utils.serialize_response(schema_out=schemas.SignUpOut)
def sign_in(email, password):
    user = users.get_user_by_email(email)
    user.verify_password(password)
    login_user(user)
    return user


#####################
#   ONLY DEV MODE   #
#####################
if backend_application.debug:
    @backend_application.route("/data/<path:filename>", methods=["GET"])
    def data(filename):
        return send_from_directory(BackendSettings.DATA_DIR, filename)
else:
    @backend_application.route("/data/<path:filename>", methods=["GET"])
    def data(filename):
        return Response("")
