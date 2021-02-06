import graphene
from graphene_django.utils.testing import GraphQLTestCase

from post_manager.comment.schema import Query


class CommentTestCase(GraphQLTestCase):
    def test_allComments_desc_order(self):
        query = """
            query {
                allComments (sortBy: "-id") {
                    id	
                    body
                }
            }
            """

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)
        self.assertIsNone(result.errors)
        self.assertEqual(500, result.data["allComments"][0]["id"])
        self.assertEqual(491, result.data["allComments"][-1]["id"])
        self.assertTrue("id" in result.data["allComments"][0])
        self.assertTrue("body" in result.data["allComments"][0])

    def test_allComments_asc_order(self):
        query = """
            query {
                allComments (sortBy: "id") {
                    id	
                    body
                }
            }
            """

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)
        self.assertIsNone(result.errors)
        self.assertEqual(1, result.data["allComments"][0]["id"])
        self.assertEqual(10, result.data["allComments"][-1]["id"])
        self.assertTrue("id" in result.data["allComments"][0])
        self.assertTrue("body" in result.data["allComments"][0])

    def test_searchComments(self):
        query = """
            query {
                searchComments (
                sortBy: "-id",
                filterName: "id"
                filterValue: "99"
                filterType: "icontains"
                ) {
                    id	
                    body
                }
            }
            """

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)
        self.assertIsNone(result.errors)
        self.assertEqual(499, result.data["searchComments"][0]["id"])
        self.assertEqual(99, result.data["searchComments"][-1]["id"])
        self.assertTrue("id" in result.data["searchComments"][0])
        self.assertTrue("body" in result.data["searchComments"][0])

    def test_searchComments_with_exact_filter(self):
        query = """
            query {
                searchComments (
                sortBy: "-id",
                filterName: "id"
                filterValue: "99"
                filterType: "exact"
                ) {
                    id	
                    body
                }
            }
            """

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)
        self.assertIsNone(result.errors)
        self.assertEqual(99, result.data["searchComments"][0]["id"])
        self.assertTrue("id" in result.data["searchComments"][0])
        self.assertTrue("body" in result.data["searchComments"][0])

    def test_searchComments_with_invalid_filtertype(self):
        query = """
            query {
                searchComments (
                sortBy: "-id",
                filterName: "id"
                filterValue: ""
                filterType: ""
                ) {
                    id	
                    body
                }
            }
            """

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)
        self.assertTrue(result.errors)

    def test_searchComments_with_pagination(self):
        query = """
            query {
                allComments (sortBy: "-id", pageNumber: 2) {
                    id	
                    body
                }
            }
            """

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)
        self.assertIsNone(result.errors)
        self.assertEqual(490, result.data["allComments"][0]["id"])
        self.assertEqual(481, result.data["allComments"][-1]["id"])
        self.assertTrue("id" in result.data["allComments"][0])
        self.assertTrue("body" in result.data["allComments"][0])
