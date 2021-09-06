import json

import Levenshtein
from loguru import logger

from decorator import catch_raise, timeit


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
    log_in_file: bool
        Логирование происходит с записью в файл.

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

    PARAMETERS = ["amount", "interest", "downpayment", "term"]
    MAX_AMOUNT = 1000000000
    MAX_TERM = 30
    BAD_REQUEST_ANSWER = {
        "double": "Параметр {param} задан дважды",
        "biggest_amount": "Превышено максимальное значение суммы кредита",
        "zero_term": "Значение срока выплаты не может быть равно 0",
        "biggest_term": "Слишком большой срок выплаты кредита",
        "greater_downpayment": "Значение первоначального взноса превышает сумму кредитования",
        "not_param": "Отсутствует значение {request_parameter} в вашем запросе",
        "bad_param": "Значение {request_parameter} должно быть числом",
    }

    def __init__(self, request_str: str, log_in_file=True):
        if log_in_file:
            logger.add("log.txt", format="{time} {level} {message}")
        self.amount, self.interest, self.downpayment, self.term = self.get_parameters(
            request_str
        )
        self.valid_param()
        logger.info("Расчет создан успешно")

    @timeit
    def get_parameters(self, request_str: str) -> tuple:
        """Получение параметров из строки запроса. Работа функции осуществляется при помощи разделения строки на списки
        с параметрами. При помощи дистанции Левенштейна определяется наличие нужных параметров в запросе. 75-процентное
        и более совпадение имени параметра в строке запроса и стандартным именем параметра (стандартные имена хранятся
        в кортеже PARAMETERS) является допустимым. Значение такого параметра будет записано с исправлением имени
        параметра. Пример: параметр "intrest" будет распознан как "interest"
        При передаче дубля параметров будет вызвано исключение.
        Функция возвращает кортеж из параметров (amount, interest, downpayment, term) с приведением значений в float.

        Parameters
        ----------
        request_str : str
            строка запроса."""
        list_request = (
            param
            for param in map(lambda x: x.split(": "), request_str.lower().split("\n"))
            if param[0]
        )
        dict_param = {}
        for key, value in list_request:
            for param in self.PARAMETERS:
                percent_coincidence = 1 - Levenshtein.distance(key, param) / max(
                    len(key), len(param)
                )
                if percent_coincidence >= 0.75:
                    if param not in dict_param:
                        dict_param[param] = value
                    else:
                        raise ValueError(
                            self.BAD_REQUEST_ANSWER["double"].format(param=param)
                        )
        dict_param["interest"] = dict_param["interest"].replace("%", "")
        return tuple(
            self.get_float_parameter(dict_param, param) for param in self.PARAMETERS
        )

    @catch_raise
    def valid_param(self):
        """Валидация параметров класса.
        Размер кредита не должен быть больше максимально возможной величины MAX_AMOUNT.
        Срок выплаты не может быть нулевым или превышать максимально допустимый MAX_TERM.
        Величина первоначального взноса не может первышать размер кредита.
        """
        if self.amount > self.MAX_AMOUNT:
            raise ValueError(self.BAD_REQUEST_ANSWER["biggest_amount"])
        if self.term == 0:
            raise ZeroDivisionError(self.BAD_REQUEST_ANSWER["zero_term"])
        elif self.term > self.MAX_TERM:
            raise ValueError(self.BAD_REQUEST_ANSWER["biggest_term"])
        if self.amount < self.downpayment:
            raise ValueError(self.BAD_REQUEST_ANSWER["greater_downpayment"])

    def get_float_parameter(self, dict_param: dict, request_parameter: str) -> float:
        """Возвращает выделенный параметр из словаря и переводит его в число с плавающей точкой.
        Если такого параметра не существует, будет вызвано исключение KeyError.
        Если величина параметра задана не в виде числа, будет вызвано исключение ValueError.
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
            raise KeyError(
                self.BAD_REQUEST_ANSWER["not_param"].format(
                    request_parameter=request_parameter
                )
            )
        except ValueError:
            raise ValueError(
                self.BAD_REQUEST_ANSWER["bad_param"].format(
                    request_parameter=request_parameter
                )
            )

    def get_percent_payment(self) -> float:
        """Возвращает общий объём начисленных процентов. Определяется по формуле:
        (Размер_кредита - первоначальный_взнос) * процентную_ставку * 0.01 * срок_выплаты"""
        return (self.amount - self.downpayment) * self.interest * 0.01 * self.term

    def get_total_payment(self) -> float:
        """Возвращает общую сумму выплаты. Определяется по формуле:
        Общий_объём_начисленных_процентов + размер_кредита - первоначальный_взнос"""
        return self.get_percent_payment() + self.amount - self.downpayment

    def get_month_payment(self) -> float:
        """Возвращает месячную выплату по кредиту. Определяется по формуле:
        Общая_сумма_выплаты / (срок_выплаты * 12)
        Результат округлен до двух знаков после запятой"""
        return round(self.get_total_payment() / self.term / 12, 2)

    def get_api(self):
        """Возвращает параметры и расчетные значения калькулятора в формате JSON"""
        return json.dumps(
            {
                "amount": self.amount,
                "interest": self.interest,
                "downpayment": self.downpayment,
                "term": self.term,
                "percent_payment": self.get_percent_payment(),
                "total_payment": self.get_total_payment(),
                "month_payment": self.get_month_payment(),
            }
        )


if __name__ == "__main__":
    credit_cal = CreditCalculator(
        "amount: 100000\ninterest: 5.5%\ndownpayment: 20000\nterm: 30\n"
    )
    print(credit_cal.get_api())
