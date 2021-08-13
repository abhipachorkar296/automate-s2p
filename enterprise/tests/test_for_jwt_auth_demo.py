# # This test file is for the demonstration of how tests can be implemented including 
# # authorization
# from django.urls import reverse
# import json
# from rest_framework.test import APITestCase
# from django.contrib.auth.hashers import make_password
# from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

# from enterprise.models import *
# from enterprise.serializers import *

# class UserModelViewTest(APITestCase):
#     def setUp(self):

#         '''
#         Populating Test DB with enterprise ID 1 and user ID 1
#         '''
#         Enterprise.objects.create(enterprise_name="ENT 1")
#         self.enterprise = Enterprise.objects.get(enterprise_id=1)
#         data = {
#             "enterprise_id": self.enterprise,
#             "user_email": "apple1@gmail.com",
#             "user_firstname": "Matt",
#             "user_lastname": "Paar",
#             "user_phonenumber": "xxxxxx91"
#         }
#         user = User.objects.create(**data)
#         data = {
#             "username": "matt",
#             "password": make_password("mattpaar"),
#             "user_id": user
#         }
#         user_auth = UserAuth.objects.create(**data)

#         # Below are the methods for login
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(AccessToken.for_user(user_auth)))
#         #self.client.force_authenticate(user=user_auth)
    
#     def test_get_valid_user(self):
#         '''
#         Getting user with ID 1
#         '''
#         response = self.client.get(reverse("enterprise:hello1"))
#         self.assertEqual(response.status_code, 200)