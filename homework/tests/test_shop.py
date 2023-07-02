"""
Протестируйте классы из модуля homework/models.py
"""
import pytest
from homework.models import Product, Cart


@pytest.fixture
def book():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def pen():
    return Product("pen", 15.4, "This is a pen", 400)


@pytest.fixture
def pencil():
    return Product("pencil", 12, "This is a pencil", 500)

@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, book, pen, pencil):
        # напишите проверки на метод check_quantity
        assert book.check_quantity(200) == True
        assert pen.check_quantity(500) == False
        with pytest.raises(ValueError):
            assert pencil.check_quantity(0) is ValueError
            assert pencil.check_quantity(-100) is ValueError

    def test_product_buy(self, book):
        # напишите проверки на метод buy
        quantity_before_purchase = book.quantity
        book.buy(50)
        assert book.quantity == quantity_before_purchase - 50

    def test_product_buy_more_than_available(self, book):
        # напишите проверки на метод buy, которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            book.buy(1001)


class TestCart:
    """
Напишите тесты на методы класса Cart
На каждый метод у вас должен получиться отдельный тест
На некоторые методы у вас может быть несколько тестов.
Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    def test_add_product(self, cart, book, pen, pencil):
        cart.add_product(book, 100)
        cart.add_product(pen, 100)
        cart.add_product(pencil, 100)
        assert cart.products[book] == 100
        assert cart.products[pen] == 100
        assert cart.products[pencil] == 100

        cart.add_product(book, 100)
        assert cart.products[book] == 200

    def test_remove_product(self, cart, book, pen, pencil):
        cart.add_product(book, 100)
        cart.remove_product(book, 30)
        assert cart.products[book] == 70

        cart.add_product(pen, 100)
        cart.remove_product(pen)
        assert pen not in cart.products

        cart.add_product(pencil, 100)
        cart.remove_product(pencil, 150)
        assert pencil not in cart.products

    def test_clear(self, cart, book, pen, pencil):
        cart.add_product(book, 100)
        cart.add_product(pen, 100)
        cart.add_product(pencil, 100)
        cart.clear()
        assert book not in cart.products
        assert pen not in cart.products
        assert pencil not in cart.products

    def test_get_total_price(self, cart, book, pen, pencil):
        cart.add_product(book, 100)
        cart.add_product(pen, 50)
        cart.add_product(pencil, 50)
        cart.get_total_price()
        assert cart.get_total_price() == 11370

    def test_buy(self, cart, book, pen, pencil):
        cart.add_product(book, 100)
        cart.buy()
        assert book.quantity == 900

        cart.add_product(pen, 800)
        with pytest.raises(ValueError):
            cart.buy()