import json
from graphene_django.utils.testing import GraphQLTestCase
from .fixtures import create_user_mutation, create_user_invalid_email_mutation
from backend.schema import schema


class TestUserSchema(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def test_user_creation_with_valid_data_succeeds(self):
        response = self.query(create_user_mutation())

        self.assertResponseNoErrors(response)
        self.assertEquals(response.status_code, 200)

    def test_user_creation_with_duplicate_email_fails(self):
        # Initial user creation
        self.query(create_user_mutation())
        response = self.query(create_user_mutation())

        response_content = json.loads(response.content.decode('utf-8'))

        self.assertResponseHasErrors(response)
        self.assertEquals(response_content['errors'][0]['field'], 'email')
        self.assertEquals(response_content['errors'][0]['message'], "User with ['email'] already exists")

    def test_user_creation_with_invalid_email_fails(self):
        response = self.query(create_user_invalid_email_mutation())

        response_content = json.loads(response.content.decode('utf-8'))

        self.assertResponseHasErrors(response)
        self.assertEquals(response_content['errors'][0]['field'], 'email')
        self.assertEquals(response_content['errors'][0]['message'], 'Enter a valid email address')