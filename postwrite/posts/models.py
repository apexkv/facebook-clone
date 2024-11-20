import uuid
from django.db import models
from rest_framework.exceptions import APIException


class User(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, db_index=True)
    full_name = models.CharField(max_length=500, db_index=True)

    def __str__(self):
        return self.full_name


class Post(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.full_name} - {self.created_at}"


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    like_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"


class PostLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def like_or_unlike_post(cls, user:User, post_id:str):
        post = Post.objects.filter(id=post_id).first()
        if not post:
            raise APIException("Post not found")
        
        post_like = cls.objects.filter(user=user, post=post).first()

        if post_like:
            post_like.delete()
            post.like_count -= 1
            post_like = None
        else:        
            post_like = cls.objects.create(user=user, post=post)
            post.like_count += 1

        post.save()

        new_post_like_count = post.like_count

        return new_post_like_count, bool(post_like)
    


class CommentLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def like_or_unlike_comment(cls, user:User, comment_id:str):
        comment = Comment.objects.filter(id=comment_id).first()
        if not comment:
            raise APIException("Comment not found")
        
        comment_like = cls.objects.filter(user=user, comment=comment).first()

        if comment_like:
            comment_like.delete()
            comment.like_count -= 1
            comment_like = None
        else:        
            comment_like = cls.objects.create(user=user, comment=comment)
            comment.like_count += 1

        comment.save()

        new_comment_like_count = comment.like_count

        return new_comment_like_count, bool(comment_like)