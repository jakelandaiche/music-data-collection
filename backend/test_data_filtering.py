# %%
import pandas as pd

# %%
dataset = pd.read_csv(
    "unbalanced_train_segments.csv",
    sep=", ",
    on_bad_lines="skip",
    skiprows=2,
    quotechar='"',
)
label_data = pd.read_csv("class_labels_indices.csv", on_bad_lines="skip")

# %%
pd.merge(
    dataset, label_data, "inner", left_on="positive_labels", right_on="mid", copy=True
)

# %%
label_data["mid"]

# %%
for labels in dataset[:10]["positive_labels"].str.strip('"').str.split(","):
    strings = []
    for label in labels:
        strings.append(
            label_data[label_data["mid"].str.match(label)]["display_name"].item()
        )
    print(strings)

# %%
dataset = dataset[dataset["positive_labels"].str.match(".*/m/04rlf.*")]
print(len(dataset))
for row in dataset.sample(10).iterrows():
    labels = row[1]["positive_labels"].strip('"').split(",")
    strings = []
    for label in labels:
        strings.append(
            label_data[label_data["mid"].str.match(label)]["display_name"].item()
        )
    print(strings)
    print(row[1])

# %%
