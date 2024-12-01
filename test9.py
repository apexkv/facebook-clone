"""
sample dataset im using for training the model is in
postwrite/dataset folder
"""

import pickle, os, datetime, threading, tqdm
from typing import List
import pandas as pd
from threading import Lock
import numpy as np
import json
import tqdm
import tensorflow as tf
from keras.api.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split
from keras.api.models import Model, Sequential
from keras.api.layers import TextVectorization, Input, Dense, Embedding, Concatenate, Flatten, Dropout


# map uuid fields to integers
user_id_map = {}
map_lock_user_id = Lock()
post_id_map = {}
map_lock_post_id = Lock()
comment_id_map = {}
map_lock_comment_id = Lock()

dtypes = {
    "user_id": "string",
    "user_full_name": "string",
    #
    "post_id": "string",
    "post_content": "string",
    "post_like_count": "float",
    "post_created_at": "string",
    "post_user_id": "string",
    #
    "post_like_id": "string",
    "post_like_created_at": "string",
    "post_like_post_id": "string",
    "post_like_user_id": "string",
    #
    "comment_id": "string",
    "comment_content": "string",
    "comment_like_count": "float",
    "comment_created_at": "string",
    "comment_post_id": "string",
    "comment_user_id": "string",
    #
    "comment_like_id": "string",
    "comment_like_created_at": "string",
    "comment_like_comment_id": "string",
    "comment_like_user_id": "string",
}


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
MODEL_DIR = os.path.join(BASE_DIR, "postwrite", "models")

dataset_path_list = [os.path.join(DATASET_DIR, file) for file in os.listdir(DATASET_DIR) if file.endswith(".csv")]
dataset_path_list.sort()

DATASET_PATH_LIST = dataset_path_list
DATASET_COUNT = len(DATASET_PATH_LIST)

processed_dir = os.path.join(DATASET_DIR, "processed")
completed_dir = os.path.join(DATASET_DIR, "completed")
os.makedirs(processed_dir, exist_ok=True)
os.makedirs(completed_dir, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

model_checkpoint = ModelCheckpoint(
    filepath=os.path.join(MODEL_DIR, "model_{epoch:02d}_{val_accuracy:.2f}.keras"),
    monitor="val_accuracy",
    save_best_only=True,
    save_weights_only=False,
    mode="max",
    verbose=1
)


def user_id_map_thread(user_ids):
    global user_id_map
    with tqdm.tqdm(total=len(user_ids)) as pbar:
        for i, user_id in enumerate(user_ids):
            with map_lock_user_id:
                if user_id not in user_id_map and user_id and type(user_id) != type(pd.NaT):
                    user_id_map[user_id] = i
                    pbar.set_description(f"{user_id} -> {i}")
            pbar.update(1)

def post_id_map_thread(post_ids):
    global post_id_map
    with tqdm.tqdm(total=len(post_ids)) as pbar:
        for i, post_id in enumerate(post_ids):
            with map_lock_post_id:
                if post_id not in post_id_map and post_id and type(post_id) != type(pd.NaT):
                    post_id_map[post_id] = i
                    pbar.set_description(f"{post_id} -> {i}")
            pbar.update(1)

def comment_id_map_thread(comment_ids):
    global comment_id_map
    with tqdm.tqdm(total=len(comment_ids)) as pbar:
        for i, comment_id in enumerate(comment_ids):
            with map_lock_comment_id:
                if comment_id not in comment_id_map and comment_id and type(comment_id) != type(pd.NaT):
                    comment_id_map[comment_id] = i
                    pbar.set_description(f"{comment_id} -> {i}")
            pbar.update(1)


processed_path_list:List[str] = []
post_vectorizer = TextVectorization(max_tokens=10000, output_sequence_length=250)
comment_vectorizer = TextVectorization(max_tokens=10000, output_sequence_length=250)

# step 1
for current_dataset, DATASET in enumerate(DATASET_PATH_LIST):
    start = datetime.datetime.now()
    dataset = pd.read_csv(DATASET, low_memory=False, dtype=dtypes)
    end = datetime.datetime.now()
    print(f"\n[{current_dataset}/{DATASET_COUNT}] Read {DATASET.split('/')[-1]} in {end - start}")

    time_columns = ["post_created_at", "comment_created_at", "post_like_created_at", "comment_like_created_at"]

    for col in time_columns:
        dataset[col] = pd.to_datetime(dataset[col], errors="coerce")
        dataset[col] = dataset[col].fillna(pd.Timestamp(0, tz="UTC"))
        dataset[col] = pd.DatetimeIndex(dataset[col]).astype(int)


    start = datetime.datetime.now()
    # map user ids to integers
    user_ids = dataset["user_id"].unique()
    post_ids = dataset["post_id"].unique()
    comment_ids = dataset["comment_id"].unique()

    user_id_thread = threading.Thread(target=user_id_map_thread, args=(user_ids,))
    post_id_thread = threading.Thread(target=post_id_map_thread, args=(post_ids,))
    comment_id_thread = threading.Thread(target=comment_id_map_thread, args=(comment_ids,))

    user_id_thread.start()
    post_id_thread.start()
    comment_id_thread.start()

    user_id_thread.join()
    post_id_thread.join()
    comment_id_thread.join()

    dataset = dataset.fillna("none")

    end = datetime.datetime.now()
    print(f"\nMapped ids in {end - start}")


    start = datetime.datetime.now()
    # vectorize post_content
    post_vectorizer.adapt(dataset["post_content"].values)
    dataset["post_content"] = post_vectorizer(dataset["post_content"].values)

    # vectorize comment_content
    comment_vectorizer.adapt(dataset["comment_content"].values)
    dataset["comment_content"] = comment_vectorizer(dataset["comment_content"].values)

    end = datetime.datetime.now()
    print(f"Vectorized {DATASET} in {end - start}")

    # Save the current dataset batch to file
    processed_file_path = os.path.join(processed_dir, f"processed_dataset_{current_dataset:04d}.csv")
    dataset.to_csv(processed_file_path, index=False)
    print(f"Saved processed dataset {current_dataset} to {processed_file_path}\n")
    processed_path_list.append(processed_file_path)


# save the maps
start = datetime.datetime.now()
with open("user_id_map.json", "w") as f:
    json.dump(user_id_map, f)
end = datetime.datetime.now()
print(f"Saved user_id_map in {end - start}")


start = datetime.datetime.now()
with open("post_id_map.json", "w") as f:
    json.dump(post_id_map, f)
end = datetime.datetime.now()
print(f"Saved post_id_map in {end - start}")


start = datetime.datetime.now()
with open("comment_id_map.json", "w") as f:
    json.dump(comment_id_map, f)
end = datetime.datetime.now()
print(f"Saved comment_id_map in {end - start}")

# save the vectorizers
start = datetime.datetime.now()
with open("post_vectorizer.pkl", "wb") as f:
    pickle.dump(post_vectorizer, f)
end = datetime.datetime.now()
print(f"Saved post_vectorizer in {end - start}")

start = datetime.datetime.now()
with open("comment_vectorizer.pkl", "wb") as f:
    pickle.dump(comment_vectorizer, f)
end = datetime.datetime.now()
print(f"Saved comment_vectorizer in {end - start}")


processed_path_list.sort()
processed_path_count = len(processed_path_list)

completed_dataset_path_list:List[str] = []


# step 2
with tqdm.tqdm(total=processed_path_count) as pbar:
    for i, processed_path in enumerate(processed_path_list):
        start = datetime.datetime.now()
        dataset = pd.read_csv(processed_path, low_memory=False)
        end = datetime.datetime.now()
        pbar.set_description(f"\n[{i}/{len(processed_path_list)}] Read {processed_path.split('/')[-1]} in {end - start}")

        start = datetime.datetime.now()
        # update those mapped id fields in the dataset
        dataset["user_id"] = dataset["user_id"].map(user_id_map)
        dataset["post_id"] = dataset["post_id"].map(post_id_map)
        dataset["comment_id"] = dataset["comment_id"].map(comment_id_map)

        # update those mapped id fields in the dataset with related fields in the dataset (post_user_id, post_like_post_id, post_like_user_id, comment_post_id, comment_user_id, comment_like_comment_id, comment_like_user_id)

        dataset["post_user_id"] = dataset["post_user_id"].map(user_id_map)
        dataset["post_like_post_id"] = dataset["post_like_post_id"].map(post_id_map)
        dataset["post_like_user_id"] = dataset["post_like_user_id"].map(user_id_map)
        dataset["comment_post_id"] = dataset["comment_post_id"].map(post_id_map)
        dataset["comment_user_id"] = dataset["comment_user_id"].map(user_id_map)
        dataset["comment_like_comment_id"] = dataset["comment_like_comment_id"].map(comment_id_map)
        dataset["comment_like_user_id"] = dataset["comment_like_user_id"].map(user_id_map)
        end = datetime.datetime.now()
        pbar.set_description(f"Updated ids in the dataset in {end - start}")


        # Save the current dataset batch to file
        start = datetime.datetime.now()
        processed_file_path = os.path.join(completed_dir, f"completed_dataset_{i:04d}.csv")
        dataset.to_csv(processed_file_path, index=False)
        end = datetime.datetime.now()
        pbar.set_description(f"[{i}/{processed_path_list}] Saved updated dataset {i} to {processed_file_path} in {end - start}\n")
        completed_dataset_path_list.append(processed_file_path)

        pbar.update(1)
    
    print(f"\nCompleted processing {processed_path_count} datasets\n")



# Define the model architecture
# post_content_input = Input(shape=(250,), dtype=tf.int32, name="post_content_input")
# comment_content_input = Input(shape=(250,), dtype=tf.int32, name="comment_content_input")

# numerical_features_input = Input(shape=(13,), name="numerical_features_input")  # Numerical features
# user_id_input = Input(shape=(1,), dtype=tf.int32, name="user_id_input")
# post_id_input = Input(shape=(1,), dtype=tf.int32, name="post_id_input")

# # Embeddings for user and post IDs
# user_embedding = Embedding(input_dim=len(user_id_map) + 1, output_dim=32, name="user_embedding")(user_id_input)
# post_embedding = Embedding(input_dim=len(post_id_map) + 1, output_dim=32, name="post_embedding")(post_id_input)

# # Flatten embeddings
# user_embedding_flatten = Flatten()(user_embedding)
# post_embedding_flatten = Flatten()(post_embedding)

# # Text vectorization and embeddings
# text_embedding_layer = Embedding(input_dim=100000, output_dim=64, name="text_embedding")

# post_text_embedded = text_embedding_layer(post_content_input)
# comment_text_embedded = text_embedding_layer(comment_content_input)

# # Flatten text embeddings
# post_text_features = Flatten()(post_text_embedded)
# comment_text_features = Flatten()(comment_text_embedded)

# # Concatenate all features
# combined_features = Concatenate(name="combined_features")([
#     post_text_features,
#     comment_text_features,
#     numerical_features_input,
#     user_embedding_flatten,
#     post_embedding_flatten
# ])

# # Fully connected layers
# x = Dense(128, activation="relu")(combined_features)
# x = Dense(64, activation="relu")(x)

# # Output layer
# output = Dense(1, activation="sigmoid", name="interaction_output")(x)

# # Define the model
# model = Model(inputs=[
#     post_content_input,
#     comment_content_input,
#     numerical_features_input,
#     user_id_input,
#     post_id_input
# ], outputs=output)

model = Sequential([
    Dense(128, activation='relu', input_shape=(16,)),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid', name="interaction_output")  # Output layer
])

# Compile the model
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# Summary of the model
model.summary()


completed_dataset_path_list = [os.path.join(completed_dir, path) for path in os.listdir(completed_dir)]

"""
 #   Column                   Non-Null Count   Dtype  
---  ------                   --------------   -----  
 0   user_id                  100000 non-null  int64  
 1   user_full_name           100000 non-null  object 
 2   post_id                  100000 non-null  int64  
 3   post_content             100000 non-null  int64  
 4   post_like_count          100000 non-null  float64
 5   post_created_at          100000 non-null  int64  
 6   post_user_id             100000 non-null  int64  
 7   post_like_id             100000 non-null  object 
 8   post_like_created_at     100000 non-null  int64  
 9   post_like_post_id        33062 non-null   float64
 10  post_like_user_id        33062 non-null   float64
 11  comment_id               100000 non-null  int64  
 12  comment_content          100000 non-null  int64  
 13  comment_like_count       100000 non-null  float64
 14  comment_created_at       100000 non-null  int64  
 15  comment_post_id          100000 non-null  int64  
 16  comment_user_id          100000 non-null  int64  
 17  comment_like_id          100000 non-null  object 
 18  comment_like_created_at  100000 non-null  int64  
 19  comment_like_comment_id  13 non-null      float64
 20  comment_like_user_id     13 non-null      float64
"""

# step 3: train the neural network model part by part with the updated datasets
for completed_dataset_path in completed_dataset_path_list:
    completed_dataset = pd.read_csv(completed_dataset_path, low_memory=False, dtype={
        "user_id": "int64",
        "user_full_name": "string",
        "post_id": "int64",
        "post_content": "int64",
        "post_like_count": "float",
        "post_created_at": "int64",
        "post_user_id": "int64",
        "post_like_id": "string",
        "post_like_created_at": "int64",
        "post_like_post_id": "float",
        "post_like_user_id": "float",
        "comment_id": "int64",
        "comment_content": "int64",
        "comment_like_count": "float",
        "comment_created_at": "int64",
        "comment_post_id": "int64",
        "comment_user_id": "int64",
        "comment_like_id": "string",
        "comment_like_created_at": "int64",
        "comment_like_comment_id": "float",
        "comment_like_user_id": "float"
    })

    # print(completed_dataset.head())
    # print(completed_dataset.info())


    # created additional binary column for interactions by checking is user liked to post, created comment or liked to comment
    completed_dataset["is_user_interacted"] = completed_dataset.apply(
        lambda x: 1 if x["post_like_user_id"] == x["user_id"] or x["comment_user_id"] == x["user_id"] or x["comment_like_user_id"] == x["user_id"] or x["comment_user_id"] == x["user_id"] else 0,
        axis=1
    )

    """
    combine all feature field for training (field X)
    post_content, post_like_count, post_created_at, post_user_id, post_like_created_at, post_like_post_id, post_like_user_id, comment_id, comment_content, comment_like_count, comment_created_at, comment_post_id, comment_user_id, comment_like_created_at, comment_like_comment_id, comment_like_user_id
    """
    X = completed_dataset[[
        "post_content", "post_like_count", "post_created_at", "post_user_id", "post_like_created_at", "post_like_post_id", "post_like_user_id",
        "comment_id", "comment_content", "comment_like_count", "comment_created_at", "comment_post_id", "comment_user_id", "comment_like_created_at", "comment_like_comment_id", "comment_like_user_id"
    ]].fillna(0).to_numpy()

    """
    combine all target field for training (field y)
    is_user_interacted, post_id, user_id
    """
    # y = completed_dataset[["is_user_interacted", "post_id", "user_id"]].fillna(0).to_numpy()
    y = completed_dataset[["is_user_interacted"]].to_numpy()


    start = datetime.datetime.now()

    # split the data into training and testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    # from here implement the neural network model training part by part with the updated datasets
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=20,
        batch_size=512,
        verbose=1,
        callbacks=[model_checkpoint]
    )

    end = datetime.datetime.now()
    print(f"Trained model on {completed_dataset_path.split('/')[-1]} in {end - start}")

    # save the model
    model_path = os.path.join(MODEL_DIR, f"post_recommendation_model.keras")
    model.save(model_path)

    print(f"Model saved to {model_path}")
   