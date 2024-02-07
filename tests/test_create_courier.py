import pytest
import allure
from faker import Faker
fake = Faker()

from data.custom_requests import CourierRequests


@allure.feature('Тест создания курьера')
class TestCreateCourier:
    @allure.title('Создание курьера с рандомным логином')
    def test_create_courier(self):
        payload = {'login': fake.name(), 'password': '12345678', 'firstname':'mike'}
        response = CourierRequests().post_create_courier(data=payload)
        assert response['ok']

    @allure.title('Создание двух одинаковых курьеров')
    def test_create_same_courier(self):
        payload = {'login': fake.name(), 'password': '12345678', 'firstname':'mike'}
        CourierRequests().post_create_courier(data=payload)

        response = CourierRequests().post_create_courier(data=payload, status=409)
        assert response["message"] == "Этот логин уже используется. Попробуйте другой."

    @pytest.mark.parametrize("schema",
                             [
                                 [None, '123445678', 'first_name'],
                                 ['random', None, 'first_name'],
                                 [None, None, 'first_name'],
                                 [None, '12345678', None],
                                 ['random', None, None]
                             ])
    @allure.title('Создание курьера без обязательных полей')
    def test_no_required_fields(self, schema, create_user_payload):
        payload = create_user_payload(login=schema[0], password=schema[1],
                                      firstname=schema[2])
        response = CourierRequests().post_create_courier(data=payload, status=400)
        assert response["message"] == "Недостаточно данных для создания учетной записи"
