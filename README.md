# Калькулятор денег и калорий
Это калькулятор для подсчёта денег и калорий. Пользовательская часть отсутствует. Написана только логика — отдельный класс для каждого из калькуляторов.
## Описание
#### Калькулятор денег умеет:
* Сохранять новую запись о расходах методом add_record()
* Считать, сколько денег потрачено сегодня методом get_today_stats()
* Определять, сколько ещё денег можно потратить сегодня в рублях, долларах или евро — метод get_today_cash_remained(currency)
* Считать, сколько денег потрачено за последние 7 дней — метод get_week_stats()
#### Калькулятор калорий умеет:
* Сохранять новую запись о приёме пищи— метод add_record()
* Считать, сколько калорий уже съедено сегодня — метод get_today_stats()
* Определять, сколько ещё калорий можно/нужно получить сегодня — метод get_calories_remained()
* Считать, сколько калорий получено за последние 7 дней — метод get_week_stats()

У калькуляторов много пересекающихся функций: они умеют хранить какие-либо записи о еде или деньгах (но по сути - всё, числа и даты), знают дневной лимит (сколько в день можно истратить денег или сколько калорий можно получить) и суммируют записи за конкретные даты. Вся эта общая функциональность заложена в родительском классе Calculator, а от него унаследовано классы CaloriesCalculator и CashCalculator.

Конструктор класса Calculator принимает один аргумент — число limit (дневной лимит трат/калорий, который задаёт пользователь). В конструкторе создаётся пустой список, в котором храняться записи (records).

Чтобы было удобнее создавать записи, для них создан отдельный класс Record.
В нём хранится: 
* Число amount (денежная сумма или количество килокалорий)
* Дата создания записи date (передаётся в явном виде в конструктор, либо присваивается значение по умолчанию — текущая дата) 
* Комментарий comment, поясняющий, на что потрачены деньги или откуда взялись калории.

## Установка
1. :EMOJICODE: Клонируем репозиторий: git clone https://github.com/maksyanya/hw_python_oop.git
- [ ] \(Optional) Open a followup issue
