import Levenshtein


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
        Возвращает выделенный параметр из словаря и переводит его в число с плавающей точкой
    get_percent_payment()
        Возвращает общий объём начисленных процентов
    get_total_payment()
        Возвращает общую сумму выплаты
    get_month_payment()
        Возвращает месячную выплату по кредиту
    valid_param()
        Валидация параметров
    get_parameters(request_str)
        Получение параметров из строки запроса.
    """
    PARAMETERS = ['amount', 'interest', 'downpayment', 'term']
    MAX_AMOUNT = 1000000000
    MAX_TERM = 30

    def __init__(self, request_str: str):
        self.amount, self.interest, self.downpayment, self.term = self.get_parameters(request_str)
        self.valid_param()

    def get_parameters(self, request_str: str) -> tuple:
        """Получение параметров

        Parameters
        ----------
        request_str : str
            строка запроса."""
        list_request = (param for param in map(lambda x: x.split(': '), request_str.lower().split('\n'))
                        if param[0])
        dict_param = {}
        for key, value in list_request:
            for param in self.PARAMETERS:
                percent_coincidence = 1 - Levenshtein.distance(key, param) / max(len(key), len(param))
                if percent_coincidence >= 0.75:
                    if param not in dict_param:
                        dict_param[param] = value
                    else:
                        raise ValueError(f"Параметр {param} задан дважды")
        dict_param['interest'] = dict_param['interest'].replace('%', '')
        return tuple(self.get_float_parameter(dict_param, param) for param in self.PARAMETERS)

    def valid_param(self):
        """Валидация параметров класса"""
        if self.amount > self.MAX_AMOUNT:
            raise ValueError('Превышено максимальное значение суммы кредита')
        if self.term == 0:
            raise ZeroDivisionError('Значение срока выплаты не может быть равно 0')
        elif self.term > self.MAX_TERM:
            raise ValueError('Слишком большой срок выплаты кредита')
        if self.amount < self.downpayment:
            raise ValueError('Значение первоначального взноса превышает сумму кредитования')

    def get_float_parameter(self, dict_param: dict, request_parameter: str) -> float:
        """Возвращает выделенный параметр из словаря и переводит его в число с плавающей точкой.
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
        return (self.amount - self.downpayment) * self.interest * 0.01 * self.term

    def get_total_payment(self) -> float:
        """Возвращает общую сумму выплаты."""
        return self.get_percent_payment() + self.amount - self.downpayment

    def get_month_payment(self) -> float:
        """Возвращает месячную выплату по кредиту."""
        return round(self.get_total_payment() / self.term / 12, 2)


if __name__ == '__main__':
    credit_cal = CreditCalculator('amount: 100000\ninterest: 5.5%\ndownpayment: 20000\nterm: 30\n')
    print(credit_cal.get_percent_payment(), credit_cal.get_total_payment(), credit_cal.get_month_payment(), sep='\n')
