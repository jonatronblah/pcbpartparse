from pathlib import Path
import polars as pl


class Loader:
    def __init__(self, output_path, input_path, group_dict, input_df=None) -> None:
        self.output_path = output_path
        self.input_path = input_path
        self.group_dict = group_dict

    def load_csv(self):
        df = pl.read_csv(self.input_path, separator=";", row_index_name="index")
        self.input_df = df.with_columns(pl.col("Parts").str.split(by=","))

    def _group_parts(self):
        df_out = {}
        idx = []
        for i in self.group_dict:
            _df = self.input_df.filter(
                pl.col("Parts")
                .list.eval(pl.element().str.starts_with(self.group_dict[i]))
                .list.any()
            )
            _df = _df.with_columns(pl.col("Parts").list.join(", "))
            df_out.update({i: _df})
            idx.extend(_df["index"].to_list())
        etc = self.input_df.filter(~pl.col("index").is_in(idx)).with_columns(
            pl.col("Parts").list.join(", ")
        )
        df_out.update({"HW.etc": etc})
        return df_out

    def export(self):
        df_out = self._group_parts()
        for i in df_out:
            df_out[i].write_csv(Path(self.output_path).joinpath(f"{i}.csv"))
