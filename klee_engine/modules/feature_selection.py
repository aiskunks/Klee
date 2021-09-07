import typing as t
import pandas as pd
from klee_engine.modules.module_base import ModuleBase


class FeatureSelection(ModuleBase):
    def process_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        print(df)
        return df

    def get_report_data(self) -> t.Dict[str, t.Any]:
        return {"yo": "COOL"}
