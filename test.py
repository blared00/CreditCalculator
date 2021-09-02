import unittest

from .main import CreditCalculator


class TestCreditCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.credit_cal = CreditCalculator("""amount: 100000\ninterest: 5.5%\ndownpayment: 20000\nterm: 30\n""")

    def test_create_calculator(self):
        self.assertEqual(self.credit_cal.amount, 100000.0)
        self.assertEqual(self.credit_cal.interest, 0.055)
        self.assertEqual(self.credit_cal.downpayment, 20000.0)
        self.assertEqual(self.credit_cal.term, 30.0)

    def test_percent_payment(self):
        self.assertEqual(self.credit_cal.get_percent_payment(), 132000.0)

    def test_total_payment(self):
        self.assertEqual(self.credit_cal.get_total_payment(), 212000.0)

    def test_month_payment(self):
        self.assertEqual(self.credit_cal.get_month_payment(), 588.89)
