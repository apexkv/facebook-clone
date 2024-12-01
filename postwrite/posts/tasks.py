from celery import shared_task
from celery.utils.log import get_task_logger



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
    


