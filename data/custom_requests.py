import json
import requests
import allure
from faker import Faker

fake = Faker()


class BaseRequests:
    host = 'https://qa-scooter.praktikum-services.ru'

    def post_request(self, url, data, status):
        response = requests.post(url=url, data=data)
        assert response.status_code == status
        if 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            return response.text

    def delete_request(self, url, data, status):
        response = requests.delete(url=url, data=data)
        assert response.status_code == status
        if 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            return response.text

    def get_request(self, url, status):
        response = requests.get(url=url)
        assert response.status_code == status
        if 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            return response.text


class CourierRequests(BaseRequests):
    courier_handler = '/api/v1/courier'
    courier_login_handler = '/api/v1/courier/login'

    @allure.step('Создаем курьера, POST запрос. ОР - статус {status}')
    def post_create_courier(self, data=None, status=201):
        url = f"{self.host}{self.courier_handler}"
        return self.post_request(url, data=data, status=status)

    @allure.step('Авторизуем курьера, POST запрос. ОР - {status}')
    def post_login_courier(self, data=None, status=200):
        url = f"{self.host}{self.courier_login_handler}"
        return self.post_request(url, data=data, status=status)

    @allure.step('Удаляем курьера, DELETE запрос. ОР - {status}')
    def delete_courier(self, courier_id=None, status=200):
        url = f"{self.host}{self.courier_handler}/{courier_id}"
        delete_payload = {"id": courier_id}
        return self.delete_request(url, data=delete_payload, status=status)


class OrderRequests(BaseRequests):
    order_handler = '/api/v1/orders'

    @allure.step('Создаем заказ, POST запрос. ОР - {status}')
    def post_create_order(self, data=None, status=201):
        url = f"{self.host}{self.order_handler}"
        return self.post_request(url, data=json.dumps(data), status=status)

    @allure.step('Получаем список заказов, GET запрос. ОР - {status}')
    def get_orders_list(self, status=200):
        url = f"{self.host}{self.order_handler}"
        return self.get_request(url, status=status)

