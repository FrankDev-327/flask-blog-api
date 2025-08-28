from connection import db  
from models.post_model import PostModel # Importing the db instance from connection.py

class PostService:
    def __init__(self):
        self.post_model = PostModel

    def getPostById(self, post_id):
        post = self.post_model.query.get(post_id)
        if post:
            return post.to_dict(), 200
        return {'message': 'Post not found'}, 404

    def getAllPosts(self):
        posts = self.post_model.query.all()
        return [post.to_dict() for post in posts], 200

    def createPost(self, postBody):
        if not postBody or 'title' not in postBody or 'content' not in postBody or 'user_id' not in postBody:
            return {'message': 'Title, content, and user_id required'}, 400  
        
        new_post = self.post_model(title=postBody['title'], content=postBody['content'], user_id=postBody['user_id'])
        try:
            db.session.add(new_post)  # Add to DB session
            db.session.commit()       # Commit changes
            return {'message': 'Post created', 'post': new_post.to_dict()}, 201
        except Exception as e:
            db.session.rollback()     # Rollback on error
            return {'message': f'Error creating post: {str(e)}'}, 500

    def put(self, post_id):
        # Logic to update an existing post
        return {'message': 'Post updated', 'post_id': post_id}, 200

    def delete(self, post_id):
        # Logic to delete a post
        return {'message': 'Post deleted', 'post_id': post_id}, 204