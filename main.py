import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Иногда можно писать тело циклов while, for или ветку if в той же
        # строке, если команда короткая. В данном случае нагляднее будет
        # использовать классический вид конструкции if <something>: else:
        # Также в конструктор в качестве значения по умолчанию лучше передавать
        # None вместо пустой строки
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment

    # Из рубрики "Можно лучше"
    # Для удобства в каждом классе лучше определять его строковое представление
    # https://metanit.com/python/tutorial/7.5.php


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Согласно рекомендациям обычные переменные именуются с маленькой буквы
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # Данную запись можно сократить до 7 > (today - record.date).days >= 0
            # Скобки в данном случае не играют никакой роли, они лишние
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # Переменные лучше именовать так, чтобы понятно было, что в них находится
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Бэкслеши для переносов не применяются. Можно посмотреть более подходящие варианты здесь
            # https://ru.stackoverflow.com/questions/1174999/Правильный-перенос-строки-в-python
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # в данном случае использование скобок излишне
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Если константы определены в классе, то нет необходимости передавать их
    # в качестве аргументов в метод класса get_today_cash_remained,
    # они будут доступны
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):

        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # Данну длинную конструкцию из нескольких сравнений можно не использовать,
        # если создать словарь, в котором ключом будет наименование получаемой
        # валюты (включая 'rub'), а значением будет являться массив из двух
        # элементов: курс и строковое представление валюты. Таким образом
        # можно будет напрямую получать необходимый курс и строковое
        # представление валюты без каскада сравнений

        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # Бэкслеши для переносов не применяются. Можно посмотреть более подходящие варианты здесь
            # https://ru.stackoverflow.com/questions/1174999/Правильный-перенос-строки-в-python
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    def get_week_stats(self):
        super().get_week_stats()
