import datetime as dt


class Record:
    '''Создаёт запись кол-ва
       денег/килокалорий и даты
       , а также комментарии к ним.
    '''
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.now = dt.datetime.now()
            self.date = self.now.date()
        else:
            date_format = '%d.%m.%Y'
            datetime = dt.datetime.strptime(date, date_format)
            self.date = datetime.date()


class Calculator:
    ''' Подсчитывает общее кол-во денег и калорий.'''
    def __init__(self, limit):
        '''Лимит денег/калорий.'''
        self.limit = limit
        self.records = []
        self.now = dt.datetime.now()

    def add_record(self, note):
        '''Сохраняет новую запись о
           расходах/приёме пищи.
        '''
        self.records.append(note)

    def get_today_stats(self):
        '''Cчитает сколько денег/калорий
           потрачено/съедено уже сегодня.
        '''
        amount = 0
        for note in self.records:
            if note.date == self.now.date():
                amount += note.amount
        return amount

    def get_week_stats(self):
        '''Считает сколько денег/калорий
           потрачено/получено за 7 дней.
        '''
        amount = 0
        today = self.now.date()
        week = today - dt.timedelta(days=7)
        for note in self.records:
            if week <= note.date <= today:
                amount += note.amount
        return amount


class CaloriesCalculator(Calculator):
    '''Подсчитывает кол-во калорий.'''
    def get_calories_remained(self):
        '''Определяет сколько ещё калорий
           можно/нужно получить сегодня.
        '''
        calories = self.limit - self.get_today_stats()
        if calories > 0:
            msg = (f'Сегодня можно съесть что-нибудь ещё, '
                   f'но с общей калорийностью не более {calories} кКал')
            return msg
        else:
            msg = 'Хватит есть!'
            return msg


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
        balance = self.limit - self.get_today_stats()
        if currency == 'rub':
            balance = round(balance, 2)
        elif currency == 'usd':
            balance = round(balance / self.USD_RATE, 2)
        elif currency == 'eur':
            balance = round(balance / self.EURO_RATE, 2)
        if balance > 0:
            msg = (f'На сегодня осталось {balance} {value}')
            return msg
        elif balance == 0:
            msg = 'Денег нет, держись'
            return msg
        else:
            balance = abs(balance)
            msg = (f'Денег нет, держись: твой долг - {balance} '
                   f'{value}')
            return msg
