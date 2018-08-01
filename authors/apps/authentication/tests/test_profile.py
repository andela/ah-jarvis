""" Test update and view profile """
import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from django.urls import reverse
from django.contrib.auth import get_user_model

from .utils import TEST_USER


class TestUserProfile(APITestCase):
    """ Test all the jwt funtions """

    client = APIClient()

    def register_user(self, user):
        """
        Register User and returns a user response
        having blank bio and image fields.
        """
        response = self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')
        response.render()
        user = json.loads(response.content)
        return user

    def test_get_profile(self):
        """
        This displays the initial user profile after registration
        """
        name = self.register_user(TEST_USER).get("user").get("username")
        url = reverse("profiles:view_profile", args=[name])
        response = self.client.get(url)
        response.render()
        profile = json.loads(response.content)
        details = profile["profile"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(details["bio"], "")

    def test_update_profile(self):
        token = self.register_user(TEST_USER).get("user").get("token")
        self.register_user(TEST_USER)

        user = {
            "user": {
                "username": "testuser2",
                "email": "jake@jake.jake2",
                "bio": "My bio",
                "image": "https://static.productionready.io/images/smiley-cyrus.png"
            }
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        response = self.client.put(
            reverse("authentication:user"),
            user,
            format="json")

        profile = json.loads(response.content)
        details = profile["user"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(details["bio"], "My bio")
