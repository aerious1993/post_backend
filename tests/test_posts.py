import json

import graphene
from graphene_django.utils.testing import GraphQLTestCase

from post_manager.post.schema import Query


class PostTestCase(GraphQLTestCase):
    def test_allposts(self):
        query = """
            query {
                allPosts (sortBy: "-id") {
                    id	
                    title
                }
            }
            """

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)
        self.assertIsNone(result.errors)
        self.assertEqual(100, result.data["allPosts"][0]["id"])
        self.assertEqual(91, result.data["allPosts"][-1]["id"])
        self.assertTrue("id" in result.data["allPosts"][0])
        self.assertTrue("title" in result.data["allPosts"][0])
        self.assertFalse("body" in result.data["allPosts"][0])

    def test_single_post(self):
        query = """
            query {
                post (id: 50) {
                    id	
                    body
                }
            }
            """

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)
        self.assertIsNone(result.errors)
        self.assertEqual(50, result.data["post"]["id"])
        self.assertTrue("id" in result.data["post"])
        self.assertTrue("body" in result.data["post"])
        self.assertFalse("title" in result.data["post"])

    def test_url(self):
        response = self.query(
            """
            query {
                post (id: 50) {
                    id	
                    body
                }
            }
            """
        )
        content = json.loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        self.assertEqual(50, content["data"]["post"]["id"])
        self.assertTrue("id" in content["data"]["post"])
        self.assertTrue("body" in content["data"]["post"])
        self.assertFalse("title" in content["data"]["post"])
