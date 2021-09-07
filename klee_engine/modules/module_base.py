import typing as t
from typing import Dict, Any
import pandas as pd


class ModuleBase:
    def __init__(self):
        self.locals = {}

    def process_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    def get_report_data(self) -> Dict[str, Any]:
        raise NotImplementedError

    @staticmethod
    def get_input_dataset(experiment_node) -> pd.DataFrame:
        if experiment_node.input_from == "default":
            dataset_path = f"{experiment_node.experiment_path}/dataset.csv"
        else:
            dataset_path = (
                f"{experiment_node.experiment_path}"
                f"/{experiment_node.input_from}"
                f"/output_dataset.csv"
            )
        return pd.read_csv(dataset_path)
