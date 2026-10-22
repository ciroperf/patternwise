class CardPayment:
    def __init__(self):
        self.charges = []

    def charge(self, email, amount):
        self.charges.append((email, amount))
        return True


class PaymentFactory:
    @staticmethod
    def create():
        return CardPayment()
