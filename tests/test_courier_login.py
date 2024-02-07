import pytest
from data.custom_requests import CourierRequests
import allure


@allure.feature('Тест авторизации курьера')
class TestCourierLogin:
    @allure.title('Авторизация курьера')
    def test_login_courier(self, create_user_payload, create_courier, login_courier):
        payload = create_user_payload(login='random', password='12345678')
        create_courier(data=payload)
        user = login_courier(data=payload)
        assert user['logged_in_courier']['id']


    @allure.title('Курьер без логина не может авторизоваться')
    def test_login_courier_without_data(self, create_user_payload, create_courier, login_courier):
        payload = create_user_payload(login='random', password='12345678', firstname='name')
        create_courier(data=payload)
        login_courier(data=payload)
        payload.pop('login')
        response = CourierRequests().post_login_courier(data=payload, status=400)
        assert response['message'] == 'Недостаточно данных для входа'

    @pytest.mark.parametrize("changed_data", ["login", "password"])
    @allure.title('Курьер с некорректными логином и паролем не может авторизоваться')
    def test_login_courier_with_wrong_data(self, changed_data, create_user_payload, make_random_value):
        payload = create_user_payload(login='random', password='random', firstname='name')
        CourierRequests().post_create_courier(data=payload)
        payload[changed_data] = make_random_value
        response = CourierRequests().post_login_courier(data=payload, status=404)
        assert response['message'] == 'Учетная запись не найдена'

    @allure.title('Удаленный курьер не может авторизоваться')
    def test_courier_cant_login_for_deleted_account(self, create_user_payload):
        payload = create_user_payload(login='random', password='random', firstname='name')
        CourierRequests().post_create_courier(data=payload)
        response = CourierRequests().post_login_courier(data=payload)
        courier_id = response["id"]
        response_delete = CourierRequests().delete_courier(courier_id=courier_id)
        response = CourierRequests().post_login_courier(data=payload, status=404)
        assert response_delete['ok'] and response["message"] == "Учетная запись не найдена"
