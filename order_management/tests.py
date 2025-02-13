from django.test import TestCase
from django.urls import reverse
from django.db.utils import IntegrityError
from decimal import Decimal
from order_management.models import Item, Order, OrderItem

class ItemModelTest(TestCase):
    def test_create_item(self):
        item = Item.objects.create(name="Pizza", price=Decimal("10.50"))
        self.assertEqual(item.name, "Pizza")
        self.assertEqual(item.price, Decimal("10.50"))

    def test_item_str(self):
        item = Item.objects.create(name="Burger", price=Decimal("5.99"))
        self.assertEqual(str(item), "Burger")

class OrderModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(table_number=5)

    def test_create_order(self):
        self.assertEqual(self.order.table_number, 5)
        self.assertEqual(self.order.status, Order.Status.PENDING)

    def test_order_str(self):
        self.assertEqual(str(self.order), f"Order {self.order.id} — Table 5")

    def test_get_abs_url(self):
        expected_url = reverse('orders:order_detail', args=[self.order.id])
        self.assertEqual(self.order.get_abs_url(), expected_url)

    def test_update_total_price(self):
        item1 = Item.objects.create(name="Soup", price=Decimal("3.00"))
        item2 = Item.objects.create(name="Salad", price=Decimal("4.00"))

        OrderItem.objects.create(order=self.order, item=item1, quantity=2)
        OrderItem.objects.create(order=self.order, item=item2, quantity=1)

        self.order.update_total_price()
        self.assertEqual(self.order.total_price, Decimal("10.00"))

    def test_cannot_modify_paid_order(self):
        self.order.status = Order.Status.PAID
        self.order.save()

        item = Item.objects.create(name="Steak", price=Decimal("20.00"))
        with self.assertRaises(ValueError):
            OrderItem.objects.create(order=self.order, item=item, quantity=1)

class OrderItemModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(table_number=1)
        self.item = Item.objects.create(name="Pasta", price=Decimal("7.99"))

    def test_create_order_item(self):
        order_item = OrderItem.objects.create(order=self.order, item=self.item, quantity=3)
        self.assertEqual(order_item.quantity, 3)
        self.assertEqual(order_item.item, self.item)
        self.assertEqual(order_item.order, self.order)

    def test_order_item_updates_total_price(self):
        OrderItem.objects.create(order=self.order, item=self.item, quantity=2)
        self.order.refresh_from_db()
        self.assertEqual(self.order.total_price, Decimal("15.98"))

    def test_cannot_modify_ready_or_paid_order(self):
        self.order.status = Order.Status.READY
        self.order.save()

        with self.assertRaises(ValueError):
            OrderItem.objects.create(order=self.order, item=self.item, quantity=1)

class OrderBreakingTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(table_number=7)
        self.item = Item.objects.create(name="Spaghetti", price=Decimal("12.50"))

    def test_create_order_without_table_number(self):
        with self.assertRaises(IntegrityError):
            Order.objects.create(table_number=None)

    def test_edit_paid_order(self):
        self.order.status = Order.Status.PAID
        self.order.save()

        with self.assertRaises(ValueError):
            OrderItem.objects.create(order=self.order, item=self.item, quantity=1)

    def test_delete_ready_order(self):
        self.order.status = Order.Status.READY
        self.order.save()

        with self.assertRaises(ValueError):
            self.order.delete()

    def test_total_price_calculation_edge_cases(self):
        OrderItem.objects.create(order=self.order, item=self.item, quantity=1000000)
        self.order.refresh_from_db()
        self.assertGreater(self.order.total_price, Decimal("10000000"))

        OrderItem.objects.create(order=self.order, item=self.item, quantity=0)
        self.order.refresh_from_db()
        self.assertGreater(self.order.total_price, Decimal("10000000"))

    def test_race_condition_total_price(self):
        OrderItem.objects.create(order=self.order, item=self.item, quantity=1)
        self.order.update_total_price()

        OrderItem.objects.create(order=self.order, item=self.item, quantity=2)
        OrderItem.objects.create(order=self.order, item=self.item, quantity=3)
        
        self.order.update_total_price()
        self.assertEqual(self.order.total_price, Decimal("12.50") * 6)