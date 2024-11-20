from celery import shared_task
from celery.utils.log import get_task_logger

import pickle
import datetime
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from .models import Post, User, Comment, PostLike, CommentLike


logger = get_task_logger(__name__)



"""
train model for for post recommendation using post content,
postlikes, comments, commentlikes, user data. this model will
take user's friends list and post list as input and return
recommended posts for user sorted by relevance.

because of the large amount of data, need to train the model
in a small batch data. so, we will train the model in a few
iterations and save the model after each iteration.
"""
@shared_task
def train_post_recommendation_model():
    logger.info("Training post recommendation model.")
    # get all posts
    posts = Post.objects.all()
    # get all users
    users = User.objects.all()
    # get all comments
    comments = Comment.objects.all()
    # get all post likes
    post_likes = PostLike.objects.all()
    # get all comment likes
    comment_likes = CommentLike.objects.all()

    # create a dataframe for posts
    post_data = pd.DataFrame(list(posts.values()))
    # create a dataframe for users
    user_data = pd.DataFrame(list(users.values()))
    # create a dataframe for comments
    comment_data = pd.DataFrame(list(comments.values()))
    # create a dataframe for post likes
    post_like_data = pd.DataFrame(list(post_likes.values()))
    # create a dataframe for comment likes
    comment_like_data = pd.DataFrame(list(comment_likes.values()))

    # prepare data for training
    # Initialize the TF-IDF Vectorizer
    tfidf = TfidfVectorizer(stop_words="english", max_features=5000)

    # vecorize post content
    post_content = tfidf.fit_transform(post_data["content"])

    # merge post data with likes and comments
    post_like_counts = post_like_data.groupby('post_id').size().reset_index(name='like_count')
    post_features = post_data.merge(post_like_counts, on='id', how='left').fillna(0)
    
    # User-post interaction (labeling: 1 for interaction, 0 otherwise)
    user_post_interaction = post_like_data[['user_id', 'post_id']]
    user_post_interaction['interaction'] = 1

    # Generate negative samples (posts that user hasn't interacted yet with)
    negative_post_samples = post_data[~post_data['id'].isin(user_post_interaction['post_id'])]
    negative_post_samples['interaction'] = 0

    # Combine negative and positive post samples
    training_data = pd.concat([user_post_interaction, negative_post_samples], ignore_index=True)

    # Merge user-post interaction data with post features
    training_data = training_data.merge(post_features, left_on='post_id', right_on='id', how='left').fillna(0)

    # Split the data into training and testing sets
    X = training_data.drop(['user_id', 'post_id', 'interaction'], axis=1) # Features
    y = training_data['interaction'] # Target variable

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model few times for get highest accuracy
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_train, y_train)

    # make predictions
    y_pred = model.predict(X_test)
    
    # evaluate model
    accuracy = accuracy_score(y_test, y_pred)
    logger.info(f"Model accuracy: {accuracy}")

    # save model with timestamp
    model_file = f"post_recommendation_model_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pkl"
    with open(model_file, "wb") as f:
        pickle.dump(model, f)


