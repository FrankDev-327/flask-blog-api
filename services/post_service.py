import json
from connection import db  
from logger.logging import LoggerApp
from models.post_model import PostModel 
from redis_serve.redis_service import RedisService

class PostService:
    def __init__(self):
        self.logger = LoggerApp()
        self.post_model = PostModel
        self.redisService = RedisService()

    def getPostById(self, post_id):
        post = self.post_model.query.get(post_id)
        if post:
            return post.to_dict(), 200
        return {'message': 'Post not found'}, 404

    def getAllPosts(self):
        keyPost = 'allPost'
        postsFromRedis = self.redisService.getTemporalInfo(keyPost)
        if postsFromRedis is not None:
            return postsFromRedis, 200

        posts = self.post_model.query.all()
        posts_dict = [post.to_dict() for post in posts]
        self.redisService.setTemporalInfo(keyPost, json.dumps(posts_dict))
        
        return posts_dict, 200

    def createPost(self, postBody):
        if not postBody or 'title' not in postBody or 'content' not in postBody or 'user_id' not in postBody:
            self.logger.logErrorInfo({'messerrorMsgage': 'Title, content, and user_id required'})
            return {'message': 'Title, content, and user_id required'}, 400  
        
        new_post = self.post_model(title=postBody['title'], content=postBody['content'], user_id=postBody['user_id'])
        try:
            db.session.add(new_post)
            db.session.commit()       
            return {'message': 'Post created', 'post': new_post.to_dict()}, 201
        except Exception as e:
            db.session.rollback()  
            self.logger.logErrorInfo({'messerrorMsgage':  'Error creating post'})
            return {'message': f'Error creating post: {str(e)}'}, 500

    def put(self, post_id):
        return {'message': 'Post updated', 'post_id': post_id}, 200

    def delete(self, post_id):
        return {'message': 'Post deleted', 'post_id': post_id}, 204