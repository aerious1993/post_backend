import graphene

import post_manager.comment.schema
import post_manager.post.schema


class Query(
    post_manager.post.schema.Query,
    post_manager.comment.schema.Query,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query)
