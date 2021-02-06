import graphene
import requests

from post_manager.utilities.graphene_filter import Filter, get_pagination_index


class Post(Filter, graphene.ObjectType):

    userId = graphene.Int()
    id = graphene.Int()
    title = graphene.String()
    body = graphene.String()


class Query(graphene.ObjectType):

    all_posts = graphene.List(
        Post, sort_by=graphene.String(), page_number=graphene.Int()
    )
    post = graphene.Field(
        Post,
        id=graphene.Int(),
    )

    def resolve_post(self, context, id=None):
        resp = requests.get(f"https://jsonplaceholder.typicode.com/posts/{id}")

        return resp.json()

    def resolve_all_posts(self, context, sort_by=None, page_number=1):
        resp = requests.get("https://jsonplaceholder.typicode.com/posts")
        posts = Post(data=resp.json())
        first, last = get_pagination_index(page_number)

        return posts.sort(sort_by)[first:last]
