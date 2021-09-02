class CreditCalculator:
    """Калькулятор для расчета выплат по кредиту

    Attributes
    ----------
    request_str : int
        Строка запроса для вычислений калькулятора.
        Каждый параметр находится на отдельной строке, а значение отделено от ключа
        двоеточием и пробелом, пустая строка в конце.
        Пример:"amount: 100000\ninterest: 5.5%\ndownpayment: 20000\nterm: 30\n"
        - размер кредита ('amount'),
        - ставка по кредиту ('interest'),
        - первоначальный взнос ('downpayment'),
        - срок в годах ('term').

    Methods
    -------
    get_float_parameter(dict_param, request_parameter)
        Сохраняет новую запись изменения расчетной величины.
    get_percent_payment()
        Возвращает общий объём начисленных процентов
    get_total_payment()
        Возвращает общую сумму выплаты
    get_month_payment()
        Возвращает месячную выплату по кредиту

    """

    def __init__(self, request_str: str):
        dict_param = dict(param for param in map(lambda x: x.split(': '), request_str.lower().split('\n')) if param[0])
        dict_param['interest'] = dict_param['interest'].replace('%', '')
        self.amount = self.get_float_parameter(dict_param, 'amount')
        self.interest = self.get_float_parameter(dict_param, 'interest') * 0.01
        self.downpayment = self.get_float_parameter(dict_param, 'downpayment')
        self.term = self.get_float_parameter(dict_param, 'term')
        if self.term == 0:
            raise ZeroDivisionError('Значение срока выплаты не может быть равно 0')
        if self.amount < self.downpayment:
            raise ValueError('Значение первоначального взноса превышает сумму кредитования')

    def get_float_parameter(self, dict_param: dict, request_parameter: str) -> float:
        """Возвращает выделеный параметр из словаря и переводит его в число с плавающей точкой.
        Parameters
        ----------
        dict_param : dict
            словарь сбора параметров
        request_parameter : str
            запрашиваемый параметр.
        """
        try:
            return float(dict_param[request_parameter].strip())
        except KeyError:
            raise KeyError(f'Отсутвует значение {request_parameter} в вашем запросе')
        except ValueError:
            raise ValueError(f'Значение {request_parameter} должно быть числом')

    def get_percent_payment(self) -> float:
        """Возвращает общий объём начисленных процентов."""
        return (self.amount - self.downpayment) * self.interest * self.term

    def get_total_payment(self) -> float:
        """Возвращает общую сумму выплаты."""
        return self.get_percent_payment() + self.amount - self.downpayment

    def get_month_payment(self) -> float:
        """Возвращает месячную выплату по кредиту."""
        return round(self.get_total_payment() / self.term / 12, 2)


if __name__ == '__main__':
    credit_cal = CreditCalculator('amount: 100000\ninterest: 5.5%\ndownpayment: 20000\nterm: 30\n')
    print(credit_cal.get_percent_payment(), credit_cal.get_total_payment(), credit_cal.get_month_payment(), sep='\n')
