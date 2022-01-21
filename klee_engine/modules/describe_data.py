import typing as t
import pandas as pd
from klee_engine.modules.module_base import ModuleBase


class DescribeData(ModuleBase):
    def process_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

    def get_report_data(self, df: pd.DataFrame) -> t.Dict[str, t.Any]:
        return {
            "report": [
                {
                    "type": "table",
                    "title": "Basic Data Statistics",
                    "data": df.describe().to_dict()
                }
            ]
        }
