import math
from connection import db
from utils.helpers import Helper
from logger.logging import LoggerApp
from models.post_model import PostModel
from models.comment_model import CommentModel
from redis_serve.redis_service import RedisService
from sqlalchemy import func, select, insert, update, delete

helper = Helper()


class PostService:
    def __init__(self):
        self.logger = LoggerApp()
        self.redisService = RedisService()

    def getPostById(self, post_id):
        try:
            stmt = select(PostModel).where(PostModel.id == post_id)
            post = db.session.execute(stmt).scalar_one_or_none()
            if post:
                return {
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,
                    "created_at": helper.formatting_time(
                        post.created_at, "%Y-%m-%d %H:%M:%S"
                    ),
                    "updated_at": helper.formatting_time(
                        post.updated_at, "%Y-%m-%d %H:%M:%S"
                    ),
                }, 200
            return {"message": "Post not found"}, 404
        except Exception as e:
            db.session.rollback()
            self.logger.logErrorInfo(
                {"messerrorMsgage": f"Error gettting post {str(e)}"}
            )
            return {"message": f"Error gettting post: {str(e)}"}, 500

    def get_post_by_title(self, post_title):
        try:
            stmt = select(PostModel).where(PostModel.title.like(f"%{post_title}%"))
            posts = db.session.execute(stmt).scalars().all()
            post_list = [
                {
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,
                    "created_at": helper.formatting_time(
                        post.created_at, "%Y-%m-%d %H:%M:%S"
                    ),
                    "updated_at": helper.formatting_time(
                        post.updated_at, "%Y-%m-%d %H:%M:%S"
                    ),
                }
                for post in posts
            ]

            return {"message": "List of posts", "post": post_list}, 200
        except Exception as e:
            db.session.rollback()
            self.logger.logErrorInfo(
                {"messerrorMsgage": f"Error gettting post byt title {str(e)}"}
            )
            return {"message": f"Error gettting post byt title: {str(e)}"}, 500

    def listAllCommentByPostId(self, post_id, page, per_page):
        try:
            stmt = (
                select(
                    PostModel.id,
                    PostModel.title,
                    CommentModel.id,
                    CommentModel.content,
                    CommentModel.created_at,
                    CommentModel.updated_at,
                )
                .join(PostModel.comments)
                .where(PostModel.id == post_id)
                .limit(per_page)
                .offset((page - 1) * per_page)
            )

            result = db.session.execute(stmt).all()
            if not result:
                return {"message": "Post not found"}, 404

            total_comments = db.session.execute(
                select(func.count()).select_from(CommentModel)
            ).scalar_one()
            total_pages = total_comments + per_page - 1

            post_id, post_title, _, _, _, _ = result[0]
            post_dict = {"id": post_id, "title": post_title, "comments": []}

            for row in result:
                _, _, comment_id, content, created_at, updated_at = row
                comment_dict = {
                    "id": comment_id,
                    "content": content,
                    "created_at": helper.formatting_time(
                        created_at, "%Y-%m-%d %H:%M:%S"
                    ),
                    "updated_at": helper.formatting_time(
                        updated_at, "%Y-%m-%d %H:%M:%S"
                    ),
                }

                post_dict["comments"].append(comment_dict)

            return {
                "message": "List of comments of a post",
                "post": post_dict,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total_comments": total_comments,
                    "total_pages": total_pages,
                },
            }, 200
        except Exception as e:
            db.session.rollback()
            self.logger.logErrorInfo(
                {"messerrorMsgage": f"Error listing post {str(e)}"}
            )
            return {"message": f"Error listing post: {str(e)}"}, 500

    def getAllPosts(self, page, per_page):
        try:
            keyPost = f"allPost:page{page}:per{per_page}"
            postsFromRedis = self.redisService.getTemporalInfo(keyPost)
            if postsFromRedis is not None:
                return {"message": "List of posts", "posts": postsFromRedis}, 200

            stmt = select(PostModel).limit(per_page).offset((page - 1) * per_page)

            posts = db.session.execute(stmt).scalars().all()
            post_list = [
                {
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,
                    "created_at": helper.formatting_time(
                        post.created_at, "%Y-%m-%d %H:%M:%S"
                    ),
                    "updated_at": helper.formatting_time(
                        post.updated_at, "%Y-%m-%d %H:%M:%S"
                    ),
                }
                for post in posts
            ]

            total_posts = db.session.execute(
                select(func.count()).select_from(PostModel)
            ).scalar_one()
            total_pages = math.ceil(total_posts / per_page)
            post_redis = {
                "message": "List of posts",
                "posts": post_list,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total_posts": total_posts,
                    "total_pages": total_pages,
                },
            }

            self.redisService.setTemporalInfo(keyPost, post_redis)
            return post_redis, 200
        except Exception as e:
            db.session.rollback()
            self.logger.logErrorInfo({"errorMessage": f"Error listing post {str(e)}"})
            return {"message": f"Error listing post: {str(e)}"}, 500

    def createPost(self, postBody):
        if (
            not postBody
            or "title" not in postBody
            or "content" not in postBody
            or "user_id" not in postBody
        ):
            self.logger.logErrorInfo(
                {"messerrorMsgage": "Title, content, and user_id required"}
            )
            return {"message": "Title, content, and user_id required"}, 400

        try:
            stmt = (
                insert(PostModel)
                .values(
                    title=postBody["title"],
                    content=postBody["content"],
                    user_id=postBody["user_id"],
                )
                .returning(PostModel)
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
                    "created_at": helper.formatting_time(
                        new_post.created_at, "%Y-%m-%d %H:%M:%S"
                    ),
                    "updated_at": helper.formatting_time(
                        new_post.updated_at, "%Y-%m-%d %H:%M:%S"
                    ),
                },
            }, 200
        except Exception as e:
            db.session.rollback()
            self.logger.logErrorInfo(
                {"messerrorMsgage": f"Error creating post {str(e)}"}
            )
            return {"message": f"Error creating post: {str(e)}"}, 500

    def updatePost(self, post_id, post_body):
        try:
            post = self.getPostById(post_id)
            if not post:
                return {"message": "Post not found"}, 404

            stmt = (
                update(PostModel)
                .values(
                    title=post_body["title"],
                    content=post_body["content"],
                )
                .returning(PostModel)
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
                    "created_at": helper.formatting_time(
                        new_post.created_at, "%Y-%m-%d %H:%M:%S"
                    ),
                    "updated_at": helper.formatting_time(
                        new_post.updated_at, "%Y-%m-%d %H:%M:%S"
                    ),
                },
            }, 200
        except Exception as e:
            db.session.rollback()
            self.logger.logErrorInfo(
                {"messerrorMsgage": f"Error updating post {str(e)}"}
            )
            return {"message": f"Error updating post: {str(e)}"}, 500

    def delete(self, post_id):
        return {"message": "Post deleted", "post_id": post_id}, 204
