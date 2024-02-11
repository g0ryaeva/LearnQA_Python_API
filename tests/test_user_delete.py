from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
import allure
import time

@allure.epic("Deleting user data cases")
class TestUserDelete(BaseCase):
    @allure.description("This test checks the impossibility of deleting data of an authorized user with id=2")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_delete_user_id2(self):
        # LOGIN
        with allure.step('Login user with id=2'):
            login_data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }
            response1 = MyRequests.post("/user/login", data=login_data)

            Assertions.assert_code_status(response1, 200)

            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")
            user_id = self.get_json_value(response1, "user_id")

        # DELETE
        with allure.step('Try to delete user with id=2'):
            response2 = MyRequests.delete(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            Assertions.assert_code_status(response2, 400)

        #GET
        with allure.step('Check that user with id=2 cannot be deleted'):
            response3 = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            expected_fields = ["username", "email", "firstName", "lastName"]
            Assertions.assert_json_has_keys(response3, expected_fields)

    @allure.description("This test checks deleting just created user")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_delete_just_created_user(self):
        #REGISTER
        with allure.step('Register user1'):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data["email"]
            firstName = register_data["firstName"]
            password = register_data["password"]
            user_id = self.get_json_value(response1, "id")

        #LOGIN
        with allure.step('Login user1'):
            login_data = {
                'email': email,
                'password': password
            }
            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        #DELETE
        with allure.step('Delete user1 by user1'):
            response3 = MyRequests.delete(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            Assertions.assert_code_status(response3, 200)

        # GET
        with allure.step('Check that user1 deleted'):
            response3 = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            assert response3.content.decode('utf-8') == 'User not found', \
                f"Unexpected content: {response3.content}"

    @allure.description("This test checks deleting another user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_another_user(self):
        # REGISTER 1
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
            password = register_data["password"]
            user_id2 = self.get_json_value(response2, "id")

        # LOGIN1
        with allure.step('Login user1'):
            login_data = {
                'email': email1,
                'password': password
            }
            response3 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response3, "auth_sid")
            token = self.get_header(response3, "x-csrf-token")

        #DELETE
        with allure.step('Delete user2 by user1'):
            response4 = MyRequests.delete(
                f"/user/{user_id2}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
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

        # GET
        with allure.step('Get user2 data by user2'):
            response6 = MyRequests.get(
                f"/user/{user_id2}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            expected_fields = ["username", "email", "firstName", "lastName"]
            Assertions.assert_json_has_keys(response6, expected_fields)
