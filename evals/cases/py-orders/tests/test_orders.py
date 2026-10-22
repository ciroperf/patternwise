import unittest

from shop.config import ConfigManager
from shop.orders import Customer, OrderProcessor


def customer(kind, country="IT"):
    return Customer("Ada", "ada@example.com", kind, "Via Roma 1", "Milano", "20100", country)


ITEMS = [{"sku": "A", "price": 100.0, "qty": 2}, {"sku": "B", "price": 50.0, "qty": 1}]


class OrderProcessorTest(unittest.TestCase):
    def test_regular_italy(self):
        self.assertEqual(OrderProcessor().process(customer("regular"), ITEMS), 312.5)

    def test_gold_abroad_express(self):
        self.assertEqual(OrderProcessor().process(customer("gold", "DE"), ITEMS, express=True), 259.5)

    def test_vip_big_order_with_coupon(self):
        items = [{"sku": "C", "price": 600.0, "qty": 1}]
        self.assertEqual(OrderProcessor().process(customer("vip"), items, coupon="WELCOME10"), 622.2)

    def test_invoice_is_kept(self):
        p = OrderProcessor()
        p.process(customer("regular"), ITEMS, gift_wrap=True)
        self.assertIn("TOTAL: 315.00", p.last_invoice)

    def test_empty_order_rejected(self):
        with self.assertRaises(ValueError):
            OrderProcessor().process(customer("regular"), [])

    def test_counts_orders(self):
        before = ConfigManager.get_instance().settings["orders_count"]
        OrderProcessor().process(customer("regular"), ITEMS)
        self.assertEqual(ConfigManager.get_instance().settings["orders_count"], before + 1)


if __name__ == "__main__":
    unittest.main()
