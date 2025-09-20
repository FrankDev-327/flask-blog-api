import json
from connection import db  
from utils.helpers import Helper
from logger.logging import LoggerApp
from models.post_model import PostModel 
from middleware.check_token import require_token
from redis_serve.redis_service import RedisService
from sqlalchemy import select, insert, update, delete, join

helper = Helper()

class PostService:
    def __init__(self):
        self.logger = LoggerApp()
        self.post_model = PostModel
        self.redisService = RedisService()

    @require_token
    def getPostById(self, post_id):
        post = self.post_model.query.get(post_id)
        if post:
            return post.to_dict(), 200
        return {'message': 'Post not found'}, 404

    @require_token
    def getAllPosts(self):
        keyPost = 'allPost'
        postsFromRedis = self.redisService.getTemporalInfo(keyPost)
        if postsFromRedis is not None:
            return postsFromRedis, 200

        posts = self.post_model.query.all()
        posts_dict = [post.to_dict() for post in posts]
        self.redisService.setTemporalInfo(keyPost, json.dumps(posts_dict))
        
        return posts_dict, 200

    @require_token
    def createPost(self, postBody):
        if not postBody or 'title' not in postBody or 'content' not in postBody or 'user_id' not in postBody:
            self.logger.logErrorInfo({'messerrorMsgage': 'Title, content, and user_id required'})
            return {'message': 'Title, content, and user_id required'}, 400  
        
        try:
            stmt = (
                insert(self.post_model).values(
                    title=postBody['title'],
                    content=postBody['content'],
                    user_id=postBody['user_id']
                ).returning(self.post_model)
            )
        
            result = db.session.execute(stmt)
            row = result.fetchone()
            db.session.commit()       
            new_post = row[0]
            
            return {
                "message": "Post created",
                "post": {
                    "id": new_post.id,
                    "title": new_post.title,
                    "content": new_post.content,
                    "user_id": new_post.user_id,
                    "created_at": helper.formatting_time(new_post.created_at, "%Y-%m-%d %H:%M:%S"),
                    "updated_at": helper.formatting_time(new_post.updated_at, "%Y-%m-%d %H:%M:%S")
                },
            }, 200
        except Exception as e:
            db.session.rollback()  
            self.logger.logErrorInfo({'messerrorMsgage':  f'Error creating post {str(e)}'})
            return {'message': f'Error creating post: {str(e)}'}, 500

    @require_token
    def put(self, post_id):
        return {'message': 'Post updated', 'post_id': post_id}, 200

    @require_token
    def delete(self, post_id):
        return {'message': 'Post deleted', 'post_id': post_id}, 204