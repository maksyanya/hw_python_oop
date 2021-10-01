import datetime as dt


class Record:
    '''Создаёт запись кол-ва
       денег/килокалорий и даты
       , а также комментарии к ним.
    '''
    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            datetime = dt.datetime.strptime(date, self.DATE_FORMAT)
            self.date = datetime.date()


class Calculator:
    ''' Подсчитывает общее кол-во денег и калорий.'''
    INTERVAL = dt.timedelta(days=7)

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, note):
        self.records.append(note)

    def get_today_stats(self):
        today = dt.date.today()
        return sum(note.amount
                   for note in self.records
                   if note.date == today)

    def get_week_stats(self):
        today = dt.date.today()
        sennight = today - self.INTERVAL
        return sum(note.amount
                   for note in self.records
                   if sennight < note.date <= today)


class CaloriesCalculator(Calculator):
    '''Подсчитывает кол-во калорий.'''
    MORE_EAT = ('Сегодня можно съесть что-нибудь ещё, '
                'но с общей калорийностью не более {amount} кКал')
    STOP_EAT = 'Хватит есть!'

    def get_calories_remained(self):
        calories = self.limit - self.get_today_stats()
        if calories > 0:
            return self.MORE_EAT.format(amount=calories)
        return self.STOP_EAT


class CashCalculator(Calculator):
    ''' Подсчитывает кол-во денег.'''
    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1.0
    OUT_CASH = 'Денег нет, держись'
    REST_CASH = 'На сегодня осталось {amount} {forex}'
    DEBT_CASH = 'Денег нет, держись: твой долг - {amount} {forex}'
    STOP_ERROR = ('Несоответствующее значение. Остановлена работа '
                  'из-за не корректного ввода денежной валюты')
    CURRENCIES = {'rub': ('руб', RUB_RATE),
                  'usd': ('USD', USD_RATE),
                  'eur': ('Euro', EURO_RATE)}

    def get_today_cash_remained(self, currency):
        if currency not in self.CURRENCIES:
            raise ValueError(self.STOP_ERROR)
        name, rate = self.CURRENCIES[currency]
        balance = self.limit - self.get_today_stats()
        if balance == 0:
            return self.OUT_CASH
        balance = round(balance / rate, 2)
        if balance > 0:
            return self.REST_CASH.format(amount=balance, forex=name)
        return self.DEBT_CASH.format(amount=abs(balance), forex=name)


if __name__ == '__main__':
    cash = CashCalculator(1000)
    cash.add_record(Record(amount=100, comment='кофе'))
    cash.add_record(Record(amount=200, comment='Серёге за обед'))
    cash.add_record(Record(amount=800, comment='Казино'))

    print(cash.get_today_cash_remained('rub'))
