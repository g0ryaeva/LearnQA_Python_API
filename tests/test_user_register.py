import string

import pytest
import random
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

@allure.epic("User creation cases")
class TestUserRegister(BaseCase):
    exclude_params = [
        ("email"),
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName")
    ]

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("This test checks creation user")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")


    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test checks creation user with existing email")
    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"
        Assertions.assert_code_status(response, 400)


    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("This test checks creation user with incorrect email")
    def test_create_user_with_incorrect_email(self):
        email = "vinkotovexample.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected response content {response.content}"
        Assertions.assert_code_status(response, 400)

    @pytest.mark.parametrize('field', exclude_params)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test checks creation user with missing field")
    def test_create_user_with_missing_field(self, field):
        data = self.prepare_registration_data()
        del data[field]

        response = MyRequests.post("/user/", data=data)

        assert response.content.decode("utf-8") == f"The following required params are missed: {field}", \
            f"Unexpected response content {response.content}"
        Assertions.assert_code_status(response, 400)

    @allure.description("This test checks creation user with short username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_short_username(self):
        data = self.prepare_registration_data()
        field = 'username'
        data[field] = random.choice(string.ascii_letters)

        response = MyRequests.post("/user/", data=data)

        assert response.content.decode("utf-8") == f"The value of '{field}' field is too short", \
            f"Unexpected response content {response.content}"
        Assertions.assert_code_status(response, 400)

    @allure.description("This test checks creation user with long username")
    @allure.label("negative")
    def test_create_user_with_long_username(self):
        data = self.prepare_registration_data()
        field = 'username'
        value = ''.join((random.choice(string.ascii_letters) for x in range(251)))
        data[field] = value

        response = MyRequests.post("/user/", data=data)

        assert response.content.decode("utf-8") == f"The value of '{field}' field is too long", \
            f"Unexpected response content {response.content}"
        Assertions.assert_code_status(response, 400)