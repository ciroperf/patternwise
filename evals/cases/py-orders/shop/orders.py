from shop.config import ConfigManager
from shop.payments import PaymentFactory


class Customer:
    def __init__(self, name, email, customer_type, street, city, zip_code, country):
        self.name = name
        self.email = email
        self.customer_type = customer_type  # "regular", "gold", "vip"
        self.street = street
        self.city = city
        self.zip_code = zip_code
        self.country = country


class OrderProcessor:
    def __init__(self):
        self.last_invoice = None
        self.processed = []

    def process(self, customer, items, coupon=None, express=False, gift_wrap=False):
        # validate
        if not items:
            raise ValueError("empty order")
        for item in items:
            if item["qty"] <= 0:
                raise ValueError("bad qty for " + item["sku"])
            if item["price"] < 0:
                raise ValueError("bad price for " + item["sku"])

        # subtotal
        subtotal = 0
        for item in items:
            subtotal = subtotal + item["price"] * item["qty"]

        # discount by customer type
        discount = 0
        if customer.customer_type == "regular":
            discount = 0
        elif customer.customer_type == "gold":
            discount = subtotal * 0.05
        elif customer.customer_type == "vip":
            discount = subtotal * 0.10
            if subtotal > 500:
                discount = discount + 20
        else:
            raise ValueError("unknown customer type")
        if coupon is not None:
            if coupon == "WELCOME10":
                discount = discount + 10
            elif coupon == "HALF":
                discount = discount + (subtotal - discount) / 2

        # shipping by customer type and country
        shipping = 0
        if customer.customer_type == "regular":
            if customer.country == "IT":
                shipping = 7.5
            else:
                shipping = 15
        elif customer.customer_type == "gold":
            if customer.country == "IT":
                shipping = 3.5
            else:
                shipping = 10
        elif customer.customer_type == "vip":
            shipping = 0
        if express:
            shipping = shipping + 12
        if gift_wrap:
            shipping = shipping + 2.5

        # tax
        taxable = subtotal - discount
        if customer.country == "IT":
            tax = taxable * 0.22
        else:
            tax = 0
        total = round(taxable + tax + shipping, 2)

        # pay
        payment = PaymentFactory.create()
        if ConfigManager.get_instance().settings["payments_enabled"]:
            payment.charge(customer.email, total)

        # invoice
        lines = []
        lines.append("INVOICE for " + customer.name)
        lines.append(customer.street + ", " + customer.zip_code + " " + customer.city + " (" + customer.country + ")")
        for item in items:
            lines.append(f"{item['sku']} x{item['qty']} @ {item['price']:.2f}")
        lines.append(f"Subtotal: {subtotal:.2f}")
        lines.append(f"Discount: {discount:.2f}")
        lines.append(f"Shipping: {shipping:.2f}")
        lines.append(f"Tax: {tax:.2f}")
        lines.append(f"TOTAL: {total:.2f}")
        self.last_invoice = "\n".join(lines)
        self.processed.append(total)
        ConfigManager.get_instance().settings["orders_count"] += 1
        return total

    def shipping_label(self, customer):
        return (customer.name + "\n" + customer.street + "\n" + customer.zip_code + " "
                + customer.city + "\n" + customer.country)

    def estimated_days(self, customer, express):
        if customer.customer_type == "vip":
            return 1
        elif customer.customer_type == "gold":
            return 1 if express else 3
        else:
            return 2 if express else 5
