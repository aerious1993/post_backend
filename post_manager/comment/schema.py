import graphene
import requests

from post_manager.utilities.graphene_filter import Filter, get_pagination_index


class Comment(Filter, graphene.ObjectType):

    postId = graphene.Int()
    id = graphene.Int()
    name = graphene.String()
    email = graphene.String()
    body = graphene.String()


class Query(graphene.ObjectType):

    all_comments = graphene.List(
        Comment, sort_by=graphene.String(), page_number=graphene.Int()
    )
    search_comments = graphene.List(
        Comment,
        sort_by=graphene.String(),
        filter_name=graphene.String(),
        filter_value=graphene.String(),
        filter_type=graphene.String(),
        page_number=graphene.Int(),
    )

    def resolve_all_comments(root, context, sort_by=None, page_number=1):

        resp = requests.get("https://jsonplaceholder.typicode.com/comments")
        comments = Comment(data=resp.json())
        first, last = get_pagination_index(page_number)

        return comments.sort(sort_by)[first:last]

    def resolve_search_comments(
        root,
        context,
        sort_by=None,
        filter_name=None,
        filter_value=None,
        filter_type=None,
        page_number=1,
    ):

        resp = requests.get("https://jsonplaceholder.typicode.com/comments")
        comments = Comment(data=resp.json())
        if filter_name:
            comments.filter_new(
                filter_name=filter_name,
                filter_value=filter_value,
                filter_type=filter_type,
            )

        first, last = get_pagination_index(page_number)

        return comments.sort(sort_by)[first:last]
