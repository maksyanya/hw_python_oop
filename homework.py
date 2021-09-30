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
    TIME_DELTA = dt.timedelta(days=7)

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, note):
        self.records.append(note)

    def get_today_stats(self):
        today = dt.date.today()
        return sum(note.amount for note in self.records if note.date == today)

    def get_week_stats(self):
        week = []
        today = dt.date.today()
        sennight = today - self.TIME_DELTA
        for note in self.records:
            if sennight < note.date <= today:
                week.append(note.amount)
        return sum(week)


class CaloriesCalculator(Calculator):
    '''Подсчитывает кол-во калорий.'''
    PHRASE = ('Сегодня можно съесть что-нибудь ещё, '
              'но с общей калорийностью не более {key_to_insert} кКал')

    def get_calories_remained(self):
        calories = self.limit - self.get_today_stats()
        if calories > 0:
            return self.PHRASE.format(key_to_insert=calories)
        return 'Хватит есть!'


class CashCalculator(Calculator):
    ''' Подсчитывает кол-во денег.'''
    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1.0
    SHORT_PHRASE = 'Денег нет, держись'
    MIDDLE_PHRASE = 'На сегодня осталось {key_first} {key_second}'
    LONG_PHRASE = 'Денег нет, держись: твой долг - {key_first} {key_second}'
    CURRENCIES = {'rub': ('руб', RUB_RATE),
                  'usd': ('USD', USD_RATE),
                  'eur': ('Euro', EURO_RATE)}

    def get_today_cash_remained(self, currency):
        if currency not in self.CURRENCIES:
            raise ValueError("Несоответствующее значение")
        currency_name, currency_rate = self.CURRENCIES[currency]
        balance = self.limit - self.get_today_stats()
        balance = round(balance / currency_rate, 2)
        if balance == 0:
            return self.SHORT_PHRASE
        if balance > 0:
            return self.MIDDLE_PHRASE.format(key_first=balance,
                                             key_second=currency_name)
        balance = abs(balance)
        return self.LONG_PHRASE.format(key_first=balance,
                                       key_second=currency_name)


cash = CashCalculator(1000)
cash.add_record(Record(amount=145, comment='кофе'))
cash.add_record(Record(amount=300, comment='Серёге за обед'))
print(cash.get_today_cash_remained('rub'))
