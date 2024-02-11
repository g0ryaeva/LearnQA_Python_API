from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure
import random

@allure.epic("Getting user data cases")
class TestUserGet(BaseCase):
    @allure.description("This test checks getting unauthorized user data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.description("This test checks getting authorized user data")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        with allure.step('Login user'):
            response1 = MyRequests.post("/user/login", data=data)

            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")
            user_id_from_auth_method = self.get_json_value(response1, "user_id")

        with allure.step('Get user data by the same user'):
            response2 = MyRequests.get(
                f"/user/{user_id_from_auth_method}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            expected_fields = ["username", "email", "firstName", "lastName"]
            Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.description("This test checks one user's login and getting another user's data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_details_another_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        with allure.step('Login user'):
            response1 = MyRequests.post("/user/login", data=data)

            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")
            user_id_from_auth_method = self.get_json_value(response1, "user_id")

        new_user_id = 1

        with allure.step('Try to get data of another user'):
            response2 = MyRequests.get(
                f"/user/{new_user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            Assertions.assert_json_has_key(response2, "username")
            Assertions.assert_json_has_not_key(response2, "email")
            Assertions.assert_json_has_not_key(response2, "firstName")
            Assertions.assert_json_has_not_key(response2, "lastName")