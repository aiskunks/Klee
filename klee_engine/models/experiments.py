from klee_engine.application import db
from klee_engine.application.settings import BackendSettings


class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    experiment_nodes = db.relationship(
        argument="ExperimentNode", backref="experiment", lazy=True
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey(column="users.id"), nullable=False
    )
    __tablename__ = "experiment"

    @property
    def experiment_path(self):
        return f"{BackendSettings.DATA_DIR}/experiments/{self.id}"

    @property
    def dataset_filepath(self):
        return f"{self.experiment_path}/dataset.csv"


class ExperimentNode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    experiment_id = db.Column(
        db.Integer, db.ForeignKey(column="experiment.id"), nullable=False
    )
    module_name = db.Column(db.String(255), nullable=False)
    input_from = db.Column(db.String(255), nullable=False)

    __tablename__ = "experiment_node"
    __table_args__ = (
        db.UniqueConstraint(
            "experiment_id", "module_name", name="unique_module_for_experiment"
        ),
    )

    @property
    def experiment_path(self):
        return f"{BackendSettings.DATA_DIR}/experiments/{self.experiment_id}"

    @property
    def module_path(self):
        return f"{self.experiment_path}/{self.module_name}"

    @property
    def input_from_filepath(self):
        if self.input_from == "default":
            return f"{self.experiment_path}/dataset.csv"

        return f"{self.experiment_path}/{self.input_from}/output_dataset.csv"
