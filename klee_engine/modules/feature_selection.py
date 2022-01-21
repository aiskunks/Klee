import typing as t
import pandas as pd
from klee_engine.modules.module_base import ModuleBase
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression


class FeatureSelection(ModuleBase):
    def process_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

    def get_report_data(self, df: pd.DataFrame) -> t.Dict[str, t.Any]:
        df = df.rename(columns={"target": "label"})
        features = df.columns.values[df.columns.values != "label"]
        X = df[features]
        y = df.label
        selector = RFE(
            estimator=LogisticRegression(penalty="l1", solver="liblinear"),
            n_features_to_select=1
        )
        selector.fit(X, y)
        bar_plot_x = list(features)
        bar_plot_y = (selector.ranking_.max() - selector.ranking_).tolist()

        return {
            "report": [
                {
                    "type": "bar_plot",
                    "title": "Feature Evaluation Plot",
                    "data": {
                        "x": bar_plot_x, "y": bar_plot_y
                    }
                }
            ]
        }
