# posts/schema.py

# posts/schema.py

import graphene
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
import graphql_jwt
from django.contrib.auth import get_user_model
from .models import Post, Vote, Comment, Reaction
from graphql import GraphQLError

User = get_user_model()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email")

class PostType(DjangoObjectType):
    comments_count = graphene.Int()
    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "game",
            "image",
            "posted_by",
            "created_at",
            "votes",
            "comments",
            "reactions",
        )
    def resolve_comments_count(self, info):
        return self.comments.count()

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote
        fields = ("id", "post", "user", "created_at")

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("id", "post", "user", "content", "created_at")

class ReactionType(DjangoObjectType):
    class Meta:
        model = Reaction
        fields = ("id", "post", "user", "reaction_type", "created_at")

class Query(graphene.ObjectType):
    me            = graphene.Field(UserType)
    all_posts     = graphene.List(PostType)
    my_posts      = graphene.List(PostType)
    all_comments  = graphene.List(CommentType, post_id=graphene.ID())
    all_reactions = graphene.List(ReactionType, post_id=graphene.ID())

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        return user

    def resolve_all_posts(self, info):
        return Post.objects.all().order_by("-created_at")

    def resolve_my_posts(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        return Post.objects.filter(posted_by=user).order_by("-created_at")

    def resolve_all_comments(self, info, post_id=None):
        qs = Comment.objects.all()
        return qs.filter(post__id=post_id) if post_id else qs

    def resolve_all_reactions(self, info, post_id=None):
        qs = Reaction.objects.all()
        return qs.filter(post__id=post_id) if post_id else qs

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    class Arguments:
        username = graphene.String(required=True)
        email    = graphene.String(required=True)
        password = graphene.String(required=True)
    def mutate(self, info, username, email, password):
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return CreateUser(user=user)

class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)
    class Arguments:
        title   = graphene.String(required=True)
        content = graphene.String(required=True)
        game    = graphene.String(required=True)
        image   = Upload(required=False)
    def mutate(self, info, title, content, game, image=None):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        post = Post(title=title, content=content, game=game, posted_by=user)
        if image:
            post.image = image
        post.save()
        return CreatePost(post=post)

class CreateVote(graphene.Mutation):
    vote = graphene.Field(VoteType)
    class Arguments:
        post_id = graphene.ID(required=True)
    def mutate(self, info, post_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        post = Post.objects.get(pk=post_id)
        vote = Vote.objects.create(post=post, user=user)
        return CreateVote(vote=vote)

class CreateComment(graphene.Mutation):
    comment = graphene.Field(CommentType)
    class Arguments:
        post_id = graphene.ID(required=True)
        content = graphene.String(required=True)
    def mutate(self, info, post_id, content):
        user    = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        post    = Post.objects.get(pk=post_id)
        comment = Comment.objects.create(post=post, user=user, content=content)
        return CreateComment(comment=comment)

class DeleteComment(graphene.Mutation):
    class Arguments:
        comment_id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, comment_id):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("No autorizado")

        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            raise GraphQLError("Comentario no encontrado")

        if comment.user != user:
            raise GraphQLError("Solo puedes borrar tus propios comentarios")

        comment.delete()
        return DeleteComment(success=True)

class CreateReaction(graphene.Mutation):
    reaction = graphene.Field(ReactionType)
    class Arguments:
        post_id       = graphene.ID(required=True)
        reaction_type = graphene.String(required=True)
    def mutate(self, info, post_id, reaction_type):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        post = Post.objects.get(pk=post_id)
        reaction, _ = Reaction.objects.update_or_create(
            post=post, user=user,
            defaults={"reaction_type": reaction_type}
        )
        return CreateReaction(reaction=reaction)

# ✅ NUEVO: Mutación para quitar reacción del usuario
class RemoveReaction(graphene.Mutation):
    success = graphene.Boolean()
    class Arguments:
        post_id = graphene.ID(required=True)
    def mutate(self, info, post_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        try:
            reaction = Reaction.objects.get(post_id=post_id, user=user)
            reaction.delete()
            return RemoveReaction(success=True)
        except Reaction.DoesNotExist:
            return RemoveReaction(success=False)

class UpdatePost(graphene.Mutation):
    post = graphene.Field(PostType)
    class Arguments:
        post_id = graphene.ID(required=True)
        title   = graphene.String(required=True)
        game    = graphene.String(required=True)
        content = graphene.String(required=True)
    def mutate(self, info, post_id, title, game, content):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        post = Post.objects.get(pk=post_id)
        if post.posted_by != user:
            raise Exception("Not allowed")
        post.title   = title
        post.game    = game
        post.content = content
        post.save()
        return UpdatePost(post=post)

class DeletePost(graphene.Mutation):
    success = graphene.Boolean()
    class Arguments:
        post_id = graphene.ID(required=True)
    def mutate(self, info, post_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        post = Post.objects.get(pk=post_id)
        if post.posted_by != user:
            raise Exception("Not allowed")
        post.delete()
        return DeletePost(success=True)

class Mutation(graphene.ObjectType):
    token_auth        = graphql_jwt.ObtainJSONWebToken.Field()
    create_user       = CreateUser.Field()
    create_post       = CreatePost.Field()
    create_vote       = CreateVote.Field()
    create_comment    = CreateComment.Field()
    create_reaction   = CreateReaction.Field()
    remove_reaction   = RemoveReaction.Field()  # ✅ Agregado aquí
    update_post       = UpdatePost.Field()
    delete_post       = DeletePost.Field()
    delete_comment    = DeleteComment.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
