import os
import json
import typing as t

from klee_engine import modules
from klee_engine.application import db
from klee_engine import models


def create_experiment(name, dataset_file, user) -> models.Experiment:
    experiment = models.Experiment(name=name, user_id=user.id)
    db.session.add(experiment)
    db.session.commit()

    os.makedirs(experiment.experiment_path)
    dataset_file.save(experiment.dataset_filepath)

    return experiment


def create_experiment_node(module_name, input_from, experiment_id) -> models.ExperimentNode:
    experiment_node = models.ExperimentNode(
        module_name=module_name,
        input_from=input_from,
        experiment_id=experiment_id
    )

    module_path = experiment_node.module_path
    os.makedirs(module_path, exist_ok=True)

    module = modules.MODULES[experiment_node.module_name](
        experiment_node=experiment_node
    )
    input_dataset = module.get_input_dataset(experiment_node)

    output_dataset = module.process_dataset(df=input_dataset)
    output_dataset.to_csv(f"{module_path}/output_dataset.csv", index=False)

    output_report = module.get_report_data(df=output_dataset)
    with open(f"{module_path}/output_report.json", "w") as json_file:
        json.dump(output_report, json_file)

    db.session.add(experiment_node)
    db.session.commit()

    return experiment_node


def create_user(**instance_kwargs) -> models.User:
    user = models.User(**instance_kwargs)
    db.session.add(user)
    db.session.commit()
    return user
