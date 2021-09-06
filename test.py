import unittest

from .main import CreditCalculator


class TestCreditCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.credit_cal = CreditCalculator("""amount: 100000\ninterest: 5.5%\ndownpayment: 20000\nterm: 30\n""")

    def test_create_calculator(self):
        self.assertEqual(self.credit_cal.amount, 100000.0)
        self.assertEqual(self.credit_cal.interest, 5.5)
        self.assertEqual(self.credit_cal.downpayment, 20000.0)
        self.assertEqual(self.credit_cal.term, 30.0)

    def test_math_func(self):
        self.assertEqual(self.credit_cal.get_percent_payment(), 132000.0)
        self.assertEqual(self.credit_cal.get_month_payment(), 588.89)
        self.assertEqual(self.credit_cal.get_total_payment(), 212000.0)

    def test_double_param_request(self):
        bad_request = "amount: 10000\ninterest: 5.5%\ndownpayment: 2000\nterm: 30\nterm: 20"
        raise_answer = "Параметр term задан дважды"
        self.assertRaisesRegex(ValueError, raise_answer, CreditCalculator, bad_request)

    def test_biggest_amount(self):
        bad_request = "amount: 10000000000\ninterest: 5.5%\ndownpayment: 2000\nterm: 30\n"
        raise_answer = "Превышено максимальное значение суммы кредита"
        self.assertRaisesRegex(ValueError, raise_answer, CreditCalculator, bad_request)

    def test_zero_term(self):
        bad_request = "amount: 100000\ninterest: 5.5%\ndownpayment: 2000\nterm: 0\n"
        raise_answer = "Значение срока выплаты не может быть равно 0"
        self.assertRaisesRegex(ZeroDivisionError, raise_answer, CreditCalculator, bad_request)

    def test_biggest_term(self):
        bad_request = "amount: 100000\ninterest: 5.5%\ndownpayment: 2000\nterm: 100\n"
        raise_answer = "Слишком большой срок выплаты кредита"
        self.assertRaisesRegex(ValueError, raise_answer, CreditCalculator, bad_request)

    def test_greater_downpayment(self):
        bad_request = "amount: 100000\ninterest: 5.5%\ndownpayment: 200000\nterm: 30\n"
        raise_answer = "Значение первоначального взноса превышает сумму кредитования"
        self.assertRaisesRegex(ValueError, raise_answer, CreditCalculator, bad_request)
