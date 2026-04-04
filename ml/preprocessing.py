import pandas as pd

def preprocess_data(path):
    # Load dataset
    df = pd.read_csv(path)

    # Optional sanity check
    assert "label" in df.columns, "Label column not found"

    # Split features and target
    X = df.drop("label", axis=1)
    y = df["label"]

    return X, y
