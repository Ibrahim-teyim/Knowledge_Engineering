import pandas as pd


class DataLoader:
    def __init__(self, to_edit_prefix, data_prefix):
        self.to_edit_prefix = to_edit_prefix
        self.data_prefix = data_prefix

    def load_csv(self, file_name):
        return pd.read_csv(self.to_edit_prefix + file_name)

    def load_csv_sample(self, file_name, nrows):
        return pd.read_csv(self.to_edit_prefix + file_name, nrows=nrows)

    def save_csv(self, df, file_name):
        df.to_csv(self.data_prefix + file_name, index=False)
