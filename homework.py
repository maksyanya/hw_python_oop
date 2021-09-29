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
            self.now = dt.datetime.now()
            self.date = self.now.date()
        else:
            datetime = dt.datetime.strptime(date, self.DATE_FORMAT)
            self.date = datetime.date()


class Calculator:
    ''' Подсчитывает общее кол-во денег и калорий.'''
    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.today = dt.date.today()
        self.period = dt.timedelta(days=7)

    def add_record(self, note):
        '''Сохраняет новую запись о
           расходах/приёме пищи.
        '''
        self.records.append(note)

    def get_today_stats(self):
        '''Cчитает сколько денег/калорий
           потрачено/съедено уже сегодня.
        '''
        day = []
        for note in self.records:
            if note.date == self.today:
                day.append(note.amount)
        return sum(day)

    def get_week_stats(self):
        '''Считает сколько денег/калорий
           потрачено/получено за 7 дней.
        '''
        week = []
        sennight = self.today - self.period
        for note in self.records:
            if sennight <= note.date <= self.today:
                week.append(note.amount)
        return sum(week)


class CaloriesCalculator(Calculator):
    '''Подсчитывает кол-во калорий.'''
    def get_calories_remained(self):
        '''Определяет сколько ещё калорий
           можно/нужно получить сегодня.
        '''
        calories = self.limit - self.get_today_stats()
        if calories > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {calories} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    ''' Подсчитывает кол-во денег.'''
    USD_RATE = 72.97
    EURO_RATE = 85.50

    def get_today_cash_remained(self, currency):
        '''Определяет сколько ещё денег можно потратить
           сегодня в рублях, долларах, или евро.
        '''
        moneys = {'rub': 'руб',
                  'usd': 'USD',
                  'eur': 'Euro'}
        value = moneys[currency]
        if currency not in moneys:
            return 'Не указана валюта!'
        balance = self.limit - self.get_today_stats()
        if currency == 'rub':
            balance = round(balance, 2)
        elif currency == 'usd':
            balance = round(balance / self.USD_RATE, 2)
        elif currency == 'eur':
            balance = round(balance / self.EURO_RATE, 2)
        else:
            balance = 0
        if balance == 0:
            return 'Денег нет, держись'
        if balance > 0:
            return (f'На сегодня осталось {balance} {value}')
        balance = abs(balance)
        return (f'Денег нет, держись: твой долг - {balance} {value}')
