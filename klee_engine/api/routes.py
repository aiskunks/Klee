import os
import json
from flask import send_from_directory, Response, request, jsonify

from klee_engine.application import backend_application
from klee_engine.application import db
from klee_engine.application.settings import BackendSettings
from klee_engine import modules
from klee_engine import models
from klee_engine.api import schemas
from klee_engine.api import route_utils
from klee_engine.api import db_constraint_handlers as handlers


@backend_application.route("/hi", methods=["GET"])
def hello_world():
    return "Hello World"


@backend_application.route("/modules", methods=["GET"])
def get_module_list():
    return {"modules": list(modules.MODULES.keys())}


@backend_application.route("/experiment/create", methods=["POST"])
@route_utils.validate_route(schema=schemas.ExperimentIn)
def create_experiment(instance: schemas.ExperimentIn):
    exp = models.Experiment(**instance.dict())
    db.session.add(exp)
    db.session.commit()

    os.makedirs(exp.experiment_path)
    dataset_file = request.files["dataset"]
    dataset_file.save(exp.dataset_filepath)

    return schemas.ExperimentOut.from_orm(exp).dict()


@backend_application.route("/experiment/<experiment_id>/node/create", methods=["POST"])
@route_utils.validate_route(
    schema=schemas.ExperimentNodeIn,
    db_constraint_handlers=[handlers.experiment_module, handlers.experiment_module_fk],
)
def create_node(instance, experiment_id):
    experiment_node = models.ExperimentNode(**instance.dict())
    db.session.add(experiment_node)
    db.session.commit()

    module_path = experiment_node.module_path
    os.makedirs(module_path, exist_ok=True)

    module = modules.MODULES[experiment_node.module_name]()
    input_dataset = module.get_input_dataset(experiment_node)

    output_dataset = module.process_dataset(df=input_dataset)
    output_dataset.to_csv(f"{module_path}/output_dataset.csv")

    output_report = module.get_report_data()
    with open(f"{module_path}/output_report.json", "w") as json_file:
        json.dump(output_report, json_file)

    return schemas.ExperimentNodeOut.from_orm(experiment_node).dict()


if backend_application.debug:

    @backend_application.route("/data/<path:filename>", methods=["GET"])
    def data(filename):
        return send_from_directory(BackendSettings.DATA_DIR, filename)


else:

    @backend_application.route("/data/<path:filename>", methods=["GET"])
    def data(filename):
        return Response("")
