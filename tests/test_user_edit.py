import string

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure
import time
import random

@allure.epic("Changing user data cases")
class TestUserEdit(BaseCase):
    @allure.description("This test checks changing firstName just created user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_just_created_user(self):
        #REGISTER
        with allure.step('Register user'):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data["email"]
            firstName = register_data["firstName"]
            password = register_data["password"]
            user_id = self.get_json_value(response1, "id")

        #LOGIN
        with allure.step('Login user'):
            login_data = {
                'email': email,
                'password': password
            }
            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        #EDIT
        with allure.step('Edit firstName by user'):
            new_name = "Changed Name"

            response3 = MyRequests.put(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": new_name}
            )

            Assertions.assert_code_status(response3, 200)

        #GET
        with allure.step('Check changing firstName of user'):
            response4 = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            Assertions.assert_json_value_by_name(
                response4,
                "firstName",
                new_name,
                "Wrong name of user after edit"
            )

    @allure.description("This test checks changing firstName unauthorized user")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("negative")
    def test_edit_unauthorized_user(self):
        #REGISTER
        with allure.step('Register user'):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data["email"]
            firstName = register_data["firstName"]
            password = register_data["password"]
            user_id = self.get_json_value(response1, "id")

        #EDIT
        with allure.step('Try to edit firstName without Login'):
            new_name = "Changed Name"

            response2 = MyRequests.put(
                f"/user/{user_id}",
                headers={},
                cookies={},
                data={"firstName": new_name}
            )

            Assertions.assert_code_status(response2, 400)

        # LOGIN
        with allure.step('Login user to check that firstName did not change'):
            login_data = {
                'email': email,
                'password': password
            }
            response3 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response3, "auth_sid")
            token = self.get_header(response3, "x-csrf-token")

        # GET
        with allure.step('Check that firstName did not change'):
            response4 = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            Assertions.assert_json_value_by_name(
                response4,
                "firstName",
                firstName,
                "Wrong name of user after edit"
            )

    @allure.description("This test checks changing firstName of another user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_another_user(self):
        #REGISTER 1
        with allure.step('Register user1'):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email1 = register_data["email"]

        time.sleep(5)

        # REGISTER 2
        with allure.step('Register user2'):
            register_data = self.prepare_registration_data()
            response2 = MyRequests.post("/user/", data=register_data)

            Assertions.assert_code_status(response2, 200)
            Assertions.assert_json_has_key(response2, "id")

            email2 = register_data["email"]
            firstName = register_data["firstName"]
            password = register_data["password"]
            user_id2 = self.get_json_value(response2, "id")

        #LOGIN1
        with allure.step('Login user1'):
            login_data = {
                'email': email1,
                'password': password
            }
            response3 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response3, "auth_sid")
            token = self.get_header(response3, "x-csrf-token")

        #EDIT
        with allure.step('Try to change user2 data by user1'):
            new_name = "Changed Name"

            response4 = MyRequests.put(
                f"/user/{user_id2}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": new_name}
            )

            Assertions.assert_code_status(response4, 200)

        # LOGIN2
        with allure.step('Login user2'):
            login_data = {
                'email': email2,
                'password': password
            }
            response5 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response5, "auth_sid")
            token = self.get_header(response5, "x-csrf-token")

        #GET
        with allure.step('Check that user2 data did not change'):
            response4 = MyRequests.get(
                f"/user/{user_id2}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            Assertions.assert_json_value_by_name(
                response4,
                "firstName",
                firstName,
                "Wrong name of user after edit"
            )

    @allure.description("This test checks changing incorrect email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_incorrect_email_user(self):
        #REGISTER
        with allure.step('Register user'):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data["email"]
            firstName = register_data["firstName"]
            password = register_data["password"]
            user_id = self.get_json_value(response1, "id")

        #LOGIN
        with allure.step('Login user'):
            login_data = {
                'email': email,
                'password': password
            }
            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        #EDIT
        with allure.step('Try to edit incorrect email'):
            new_email = "abcdeexample.com"

            response3 = MyRequests.put(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"email": new_email}
            )

            Assertions.assert_code_status(response3, 400)

        #GET
        with allure.step('Check that email did not change'):
            response4 = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            Assertions.assert_json_value_by_name(
                response4,
                "email",
                email,
                "Wrong email after edit"
            )

    @allure.description("This test checks changing short firstName")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_short_name_user(self):
        #REGISTER
        with allure.step('Register user'):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data["email"]
            firstName = register_data["firstName"]
            password = register_data["password"]
            user_id = self.get_json_value(response1, "id")

        #LOGIN
        with allure.step('Login user'):
            login_data = {
                'email': email,
                'password': password
            }
            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        #EDIT
        with allure.step('Try to edit incorrect (short) firstName'):
            new_name = random.choice(string.ascii_letters)

            response3 = MyRequests.put(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": new_name}
            )

            Assertions.assert_code_status(response3, 400)

        #GET
        with allure.step('Check that firstName did not change'):
            response4 = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            Assertions.assert_json_value_by_name(
                response4,
                "firstName",
                firstName,
                "Wrong name of user after edit"
            )