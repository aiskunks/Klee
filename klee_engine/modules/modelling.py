import os
import typing as t
import h2o
from h2o.automl import H2OAutoML
import pandas as pd
from klee_engine.modules.module_base import ModuleBase


class Modelling(ModuleBase):
    def process_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        h2o.init()
        data_path = self.experiment_node.input_from_filepath
        df = pd.read_csv(data_path)
        df_h2o = h2o.import_file(data_path)
        # define the independent and dependent variable
        y = "target"
        df_h2o[y] = df_h2o[y].asfactor()
        # split the data into train and test split
        splits = df_h2o.split_frame(ratios=[0.8], seed=1)
        train = splits[0]
        test = splits[1]
        aml = H2OAutoML(max_runtime_secs=60, seed=1, project_name="Klee")
        aml.train(y=y, training_frame=train, leaderboard_frame=test)
        self.locals["aml"] = aml
        return df

    def get_report_data(self, df: pd.DataFrame) -> t.Dict[str, t.Any]:
        leaderboard_df = self.locals["aml"].leaderboard.as_data_frame()
        # x = list(leaderboard_df.index.values)
        # y = list(leaderboard_df["auc"].values)
        report = {
            "report": [
                {
                    "type": "table",
                    "title": "AUC score Model Leaderboard",
                    "data": leaderboard_df.to_dict()
                }
            ]
        }
        h2o.cluster().shutdown()
        return report
