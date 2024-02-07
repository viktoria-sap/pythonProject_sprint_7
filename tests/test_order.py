import pytest
import allure

from data.custom_requests import OrderRequests


@allure.feature('Тест создания заказов')
class TestOrderOptions:
    @allure.title('Создание заказа с цветом {color} и без цвета')
    @pytest.mark.parametrize('color', [['BLACK'], ['GREY'], ['BLACK', 'GREY'], []])
    def test_create_order(self, color, create_order_payload):
        payload = create_order_payload
        payload["color"] = color
        response = OrderRequests().post_create_order(data=payload)
        assert "track" in response.keys()

    @allure.title('Получение списка заказов')
    def test_get_orders(self):
        response = OrderRequests().get_orders_list()
        assert "orders" in response.keys()
