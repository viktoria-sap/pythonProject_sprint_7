import pytest
from faker import Faker
import allure
from data.custom_requests import CourierRequests

fake = Faker()


@pytest.fixture
def create_user_payload():
    @allure.step('Собираем payload для пользователя')
    def _create_user_payload(login=None, password=None, firstname=None):
        payload = {}
        if login == 'random':
            payload["login"] = fake.name()
        elif login is not None:
            payload["login"] = login
        if password == 'random':
            payload["password"] = fake.pyint()
        elif password is not None:
            payload["password"] = password
        if firstname == 'random':
            payload["firstName"] = fake.name()
        elif firstname is not None:
            payload["firstName"] = firstname
        return payload

    return _create_user_payload


@pytest.fixture
@allure.step('Создаем случайное число')
def make_random_value():
    return fake.pyint()


@pytest.fixture
@allure.step('Собираем payload для отправки заказа')
def create_order_payload():
    payload = {"firstName": fake.first_name(), "lastName": fake.last_name(),
               "address": fake.address(), "metroStation": 1, "phone": "+7 123 456 78 99", "rentTime": 1,
               "deliveryDate": "2024-01-15",
               "comment": "Hello, world"}
    return payload


@pytest.fixture(scope='function')
def create_courier_and_login():
    courier = {}

    def _create_courier(data):
        nonlocal courier
        courier_requests = CourierRequests()
        created_courier = courier_requests.post_create_courier(data=data)
        logged_in_courier = courier_requests.post_login_courier(data=data)
        courier = {"created_courier": created_courier, "logged_in_courier": logged_in_courier}
        return courier

    yield _create_courier
    CourierRequests().delete_courier(courier_id=courier['logged_in_courier']['id'])
