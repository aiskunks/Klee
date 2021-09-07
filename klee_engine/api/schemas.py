import typing as t
from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from klee_engine.models import Experiment, ExperimentNode

_ExperimentIn = sqlalchemy_to_pydantic(Experiment, exclude=["id"])
_ExperimentNodeIn = sqlalchemy_to_pydantic(ExperimentNode, exclude=["id"])


class ExperimentNodeIn(_ExperimentNodeIn):
    input_from: t.Optional[str]


class ExperimentIn(_ExperimentIn):
    experiment_nodes: t.List[ExperimentNodeIn] = []


class ExperimentOutSmall(_ExperimentIn):
    id: int


class ExperimentNodeOut(ExperimentNodeIn):
    id: int


class ExperimentOut(ExperimentIn):
    id: int
    experiment_nodes: t.List[ExperimentNodeOut] = []


class ExperimentOutList(BaseModel):
    experiments: t.List[ExperimentOutSmall]
