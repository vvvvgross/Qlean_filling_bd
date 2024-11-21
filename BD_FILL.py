import psycopg2
from psycopg2 import Error
from faker import Faker
import random
from datetime import datetime, timedelta

# Настройки подключения к базе данных
conn = psycopg2.connect(
    dbname="Qlean",
    user="postgres",
    password="ii1278vqw",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

fake = Faker('ru_RU')

AMOUNT_USERS = 10000
AMOUNT_EMPLOYEES = 2000
AMOUNT_PAYMENT_METHODS = 5000
AMOUNT_PRODUCTS = 70000
AMOUNT_SERVICES = 70000

additional_services_list = [
    "Дезинфекция ковров",
    "Удаление запахов",
    "Полировка полов",
    "Использование экологичных средств",
    "Очистка труднодоступных мест",
    "Пылеудаление",
    "Обеззараживание помещений",
    "Обработка антистатиком",
    "Уход за растениями",
    "Уборка прилегающей территории",
    "Очистка вентиляционных решеток",
    "Удаление плесени",
    "Дополнительная уборка кухни",
    "Протирка плинтусов",
    "Мытье фасадов"
]

def fill_users():
    batch_size = 10000
    total_inserted = 0

    for batch_start in range(0, AMOUNT_USERS, batch_size):
        values_list = []
        batch_end = min(batch_start + batch_size, AMOUNT_USERS)
        for idx in range(batch_start, batch_end):
            name = fake.first_name()[:100]
            last_name = fake.last_name()[:100]

            # Генерация уникального номера телефона
            phone = f"+7{9000000000 + idx}"

            # Генерация уникального email
            email = f"user{idx}@example.com"

            password = fake.password()[:255]

            # Генерация случайной даты регистрации
            registration_date = fake.date_time_between(start_date='-1y', end_date='now')

            values_list.append((name, last_name, phone, email, password, registration_date))

        query = 'INSERT INTO users (name, last_name, phone, email, password, registration_date) VALUES (%s, %s, %s, %s, %s, %s);'
        cursor.executemany(query, values_list)
        conn.commit()
        total_inserted += len(values_list)
        print(f"Вставлено {total_inserted} пользователей")

    print(f"Таблица 'users' заполнена {total_inserted} записями.")
    return

def fill_employee():
    batch_size = 10000
    total_inserted = 0

    for batch_start in range(0, AMOUNT_EMPLOYEES, batch_size):
        values_list = []
        batch_end = min(batch_start + batch_size, AMOUNT_EMPLOYEES)
        for idx in range(batch_start, batch_end):
            name = fake.first_name()[:100]
            last_name = fake.last_name()[:100]

            # Генерация уникального номера телефона
            phone = f"+7{8000000000 + idx}"

            # Генерация уникального email
            email = f"employee{idx}@example.com"

            # Генерация случайной даты регистрации
            registration_date = fake.date_time_between(start_date='-1y', end_date='now')

            values_list.append((name, last_name, phone, email, registration_date))

        query = 'INSERT INTO employee (name, last_name, phone, email, registration_date) VALUES (%s, %s, %s, %s, %s);'
        cursor.executemany(query, values_list)
        conn.commit()
        total_inserted += len(values_list)
        print(f"Вставлено {total_inserted} сотрудников")

    print(f"Таблица 'employee' заполнена {total_inserted} записями.")
    return

def fill_payment_method():
    bank_names = [
        'Сбербанк', 'ВТБ', 'Альфа-Банк', 'Газпромбанк', 'Тинькофф',
        'Россельхозбанк', 'Райффайзенбанк', 'Росбанк', 'Промсвязьбанк', 'Юникредит Банк',
        'Банк Открытие', 'Московский Кредитный Банк', 'Совкомбанк', 'МТС Банк',
        'Бинбанк', 'Абсолют Банк', 'Банк Санкт-Петербург', 'Банк Зенит',
        'Ситибанк', 'Хоум Кредит Банк', 'Банк Уралсиб', 'Банк Восточный',
        'Банк Авангард', 'Банк Траст', 'Банк Левобережный', 'ТрансКапиталБанк',
        'Экспобанк', 'Межтопэнергобанк', 'Московский Индустриальный Банк', 'СМП Банк'
    ]

    batch_size = 10000
    total_inserted = 0

    for batch_start in range(0, AMOUNT_PAYMENT_METHODS, batch_size):
        values_list = []
        batch_end = min(batch_start + batch_size, AMOUNT_PAYMENT_METHODS)
        for _ in range(batch_start, batch_end):
            is_cash = random.random() < 0.3  # 30% наличными
            if is_cash:
                # Оплата наличными
                cash = True
                card = False
                bank_name = None
                card_number = None
                cvv = None
                name = None
                expiration_date = None
            else:
                # Оплата картой
                cash = False
                card = True
                bank_name = random.choice(bank_names)
                card_number = ''.join(random.choices('0123456789', k=16))
                cvv = ''.join(random.choices('0123456789', k=3))
                name = f"{fake.first_name()} {fake.last_name()}"
                expiration_date = fake.date_between(start_date='today', end_date='+5y')

            values_list.append((card, cash, bank_name, card_number, cvv, name, expiration_date))

        query = 'INSERT INTO payment_method (card, cash, bank_name, card_number, cvv, name, expiration_date) VALUES (%s, %s, %s, %s, %s, %s, %s);'
        cursor.executemany(query, values_list)
        conn.commit()
        total_inserted += len(values_list)
        print(f"Вставлено {total_inserted} платежных методов")

    print(f"Таблица 'payment_method' заполнена {total_inserted} записями.")
    return

def fill_service():
    batch_size = 10000
    total_inserted = 0
    actions = [
        "Уборка", "Чистка", "Мытье", "Дезинфекция", "Полировка", "Ремонт",
        "Химчистка", "Пылесосная уборка", "Обеззараживание", "Удаление пятен",
        "Вывоз мусора", "Обработка"
    ]
    objects = [
        "ковров", "окон", "мебели", "ванной комнаты", "кухни", "пола",
        "штор", "офисных помещений", "санузлов", "техники", "плитки",
        "ковровых покрытий", "стен", "потолков", "матрасов", "кожаной мебели",
        "посуды", "бытовой техники", "жалюзи", "сантехники", "кондиционеров"
    ]

    for batch_start in range(0, AMOUNT_SERVICES, batch_size):
        values_list = []
        batch_end = min(batch_start + batch_size, AMOUNT_SERVICES)
        for _ in range(batch_start, batch_end):
            action = random.choice(actions)
            obj = random.choice(objects)
            title = f"{action} {obj}"

            # Генерируем описание на основе названия
            description_phrases = [
                f"Профессиональное {action.lower()} {obj} с использованием современных средств.",
                f"{action} {obj} с гарантией качества.",
                f"Быстрое и эффективное {action.lower()} {obj}.",
                f"Качественное {action.lower()} {obj} по доступной цене.",
                f"Экспертное {action.lower()} {obj} с использованием безопасных материалов.",
                f"Специализированное {action.lower()} {obj} для вашего комфорта.",
                f"{action} {obj} любой сложности.",
                f"Комплексное {action.lower()} {obj} в короткие сроки."
            ]
            description = random.choice(description_phrases)

            price = round(random.uniform(50.0, 1000.0), 2)
            duration = random.randint(30, 240)  # Продолжительность в минутах

            # Случайный выбор дополнительных услуг
            num_additional_services = random.randint(1, 3)
            additional_services = random.sample(additional_services_list, num_additional_services)
            additional_services_str = ', '.join(additional_services)

            values_list.append((title, description, price, duration, additional_services_str))

        query = 'INSERT INTO service (title, description, price, duration, additional_services) VALUES (%s, %s, %s, %s, %s);'
        cursor.executemany(query, values_list)
        conn.commit()
        total_inserted += len(values_list)
        print(f"Вставлено {total_inserted} услуг")

    print(f"Таблица 'service' заполнена {total_inserted} записями.")
    return

def fill_products():
    batch_size = 10000
    total_inserted = 0
    adjectives = [
        "Антибактериальное", "Эффективное", "Экологичное", "Мощное", "Универсальное",
        "Быстродействующее", "Профессиональное", "Безопасное", "Натуральное", "Супер",
        "Концентрированное", "Ультра", "Сильнодействующее", "Гипоаллергенное", "Ароматное"
    ]
    product_types = [
        "средство", "порошок", "гель", "спрей", "шампунь", "пена", "жидкость", "кондиционер",
        "очиститель", "дезинфектор", "полироль", "эмульсия", "крем"
    ]
    usage_types = [
        "для мытья посуды", "для чистки ковров", "для уборки", "для ванной", "для кухни",
        "для стекол", "для полов", "для мебели", "для туалета", "для окон",
        "для духовых шкафов", "для плит", "для сантехники", "для стен", "для потолков"
    ]

    fragrances = [
        "с ароматом лимона", "с запахом свежести", "с ароматом лаванды", "без запаха",
        "с ароматом апельсина", "с ароматом мяты", "с цветочным ароматом", "с ароматом морского бриза"
    ]

    features = [
        "быстрое действие", "экономичный расход", "глубокое очищение", "удаление жира",
        "устранение запахов", "защита от бактерий", "не оставляет разводов", "бережный уход за поверхностями"
    ]

    for batch_start in range(0, AMOUNT_PRODUCTS, batch_size):
        values_list = []
        batch_end = min(batch_start + batch_size, AMOUNT_PRODUCTS)
        for _ in range(batch_start, batch_end):
            adjective = random.choice(adjectives)
            product_type = random.choice(product_types)
            usage = random.choice(usage_types)
            fragrance = random.choice(fragrances)
            feature = random.choice(features)

            title = f"{adjective} {product_type} {usage}"
            description = f"{title.capitalize()} {fragrance}, обеспечивает {feature}. Идеально подходит для ежедневного использования."

            price = round(random.uniform(50.0, 500.0), 2)

            values_list.append((title, description, price))

        query = 'INSERT INTO products (title, description, price) VALUES (%s, %s, %s);'
        cursor.executemany(query, values_list)
        conn.commit()
        total_inserted += len(values_list)
        print(f"Вставлено {total_inserted} продуктов")

    print(f"Таблица 'products' заполнена {total_inserted} записями.")
    return

def fill_orders(user_ids, employee_ids, payment_ids):
    batch_size = 1000  
    total_inserted = 0
    order_ids = []

    for batch_start in range(0, len(user_ids), batch_size):
        values_list = []
        batch_end = min(batch_start + batch_size, len(user_ids))
        print(f"Обработка пользователей с {batch_start} по {batch_end}")
        for user_id in user_ids[batch_start:batch_end]:
            num_orders = random.randint(1, 30)
            for _ in range(num_orders):
                employee_id = random.choice(employee_ids)
                payment_id = random.choice(payment_ids)
                order_date = fake.date_time_between(start_date='-1y', end_date='now')
                values_list.append((user_id, employee_id, payment_id, order_date))

        print(f"Количество заказов для вставки: {len(values_list)}")

        if not values_list:
            print("Список заказов для вставки пуст.")
            continue

        try:
            cursor.execute('SELECT MAX(order_id) FROM orders')
            max_order_id_before = cursor.fetchone()[0]
            if max_order_id_before is None:
                max_order_id_before = 0

            query = 'INSERT INTO orders (user_id, employee_id, payment_method, order_date) VALUES (%s, %s, %s, %s);'
            cursor.executemany(query, values_list)
            conn.commit()

            cursor.execute('SELECT MAX(order_id) FROM orders')
            max_order_id_after = cursor.fetchone()[0]

            num_inserted = max_order_id_after - max_order_id_before
            batch_order_ids = list(range(max_order_id_before + 1, max_order_id_after + 1))
            order_ids.extend(batch_order_ids)
            total_inserted += num_inserted
            print(f"Вставлено всего заказов: {total_inserted}")
        except Exception as e:
            conn.rollback()
            print(f"Ошибка при вставке заказов: {e}")
            # Дополнительный вывод для отладки
            print(f"Количество заказов в текущем batch-е: {len(values_list)}")
            print(f"Пример данных: {values_list[:5]}")  # Показать первые 5 записей
            break  # Прерываем цикл при ошибке для дальнейшей отладки

    print(f"Таблица 'orders' заполнена {len(order_ids)} записями.")
    return order_ids

def fill_address(order_ids):
    batch_size = 10000
    total_inserted = 0
    address_ids = []

    for batch_start in range(0, len(order_ids), batch_size):
        values_list = []
        batch_end = min(batch_start + batch_size, len(order_ids))
        for order_id in order_ids[batch_start:batch_end]:
            city = fake.city()[:100]
            region = fake.region()[:100]
            street = fake.street_name()[:100]
            building_number = fake.building_number()[:10]
            apartment_number = str(random.randint(1, 300))
            floor_number = random.randint(1, 20)

            values_list.append((order_id, city, region, street, building_number, apartment_number, floor_number))

        try:
            query = 'INSERT INTO address (order_id, city, region, street, building_number, apartment_number, floor_number) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING address_id;'
            cursor.executemany(query, values_list)
            conn.commit()

            cursor.execute('SELECT MAX(address_id) FROM address')
            max_address_id = cursor.fetchone()[0]
            address_ids.extend(range(max_address_id - len(values_list) + 1, max_address_id + 1))

            total_inserted += len(values_list)
            print(f"Вставлено {total_inserted} адресов")
        except Exception as e:
            conn.rollback()
            print(f"Ошибка при вставке адресов: {e}")

    print(f"Таблица 'address' заполнена {len(address_ids)} записями.")
    return address_ids

def fill_user_have_addresses(user_ids, address_ids):
    batch_size = 10000
    total_inserted = 0

    for batch_start in range(0, len(user_ids), batch_size):
        values_list = []
        batch_end = min(batch_start + batch_size, len(user_ids))
        for user_id in user_ids[batch_start:batch_end]:
            num_addresses = random.randint(1, 3)
            user_addresses = random.choices(address_ids, k=num_addresses)
            for address_id in user_addresses:
                values_list.append((user_id, address_id))

        query = 'INSERT INTO user_have_addresses (user_id, address_id) VALUES (%s, %s);'
        cursor.executemany(query, values_list)
        conn.commit()
        total_inserted += len(values_list)
        print(f"Вставлено {total_inserted} записей в user_have_addresses")

    print(f"Таблица 'user_have_addresses' заполнена {total_inserted} записями.")
    return

def fill_review(user_ids, employee_ids):
    batch_size = 10000
    total_inserted = 0

    review_texts = [
        "Отличная работа, дом сияет чистотой!",
        "Очень доволен результатом уборки.",
        "Профессионально и быстро, рекомендую.",
        "Уборка проведена качественно, спасибо!",
        "Не совсем доволен результатом.",
        "Уборка могла быть лучше.",
        "Сотрудник опоздал, но работу выполнил хорошо.",
        "Качественная чистка ковров, как новые!",
        "Мебель после чистки выглядит отлично.",
        "Благодарю за оперативность и качество.",
        "Уборка оставляет желать лучшего.",
        "Превзошли все ожидания, спасибо!",
        "Работа выполнена на отлично!",
        "Хороший сервис, буду обращаться еще.",
        "Ставлю твердую четверку, есть над чем работать."
    ]

    for batch_start in range(0, len(user_ids), batch_size):
        values_list = []
        batch_end = min(batch_start + batch_size, len(user_ids))
        for user_id in user_ids[batch_start:batch_end]:
            num_reviews = random.randint(1, 10)
            for _ in range(num_reviews):
                employee_id = random.choice(employee_ids)
                text = random.choice(review_texts)
                if "отлично" in text.lower() or "превзошли" in text.lower() or "рекомендую" in text.lower():
                    grade = 5
                elif "доволен" in text.lower() or "хороший" in text.lower() or "качественно" in text.lower():
                    grade = 4
                elif "могла быть лучше" in text.lower() or "опоздал" in text.lower():
                    grade = 3
                elif "не совсем доволен" in text.lower() or "оставляет желать лучшего" in text.lower():
                    grade = 2
                else:
                    grade = random.randint(1, 5)
                review_time = fake.time()
                review_date = fake.date_between(start_date='-1y', end_date='today')

                values_list.append((user_id, employee_id, review_date, text, grade, review_time))

        query = 'INSERT INTO review (user_id, employee_id, date, text, grade, time) VALUES (%s, %s, %s, %s, %s, %s);'
        cursor.executemany(query, values_list)
        conn.commit()
        total_inserted += len(values_list)
        print(f"Вставлено {total_inserted} отзывов")

    print(f"Таблица 'review' заполнена {total_inserted} записями.")
    return

def fill_status(order_ids):
    batch_size = 10000
    total_inserted = 0

    status_names = ['Pending', 'In Progress', 'Completed', 'Cancelled']

    for batch_start in range(0, len(order_ids), batch_size):
        values_list = []
        batch_end = min(batch_start + batch_size, len(order_ids))
        for order_id in order_ids[batch_start:batch_end]:
            num_statuses = random.randint(1, 4)
            status_sequence = random.choices(status_names, k=num_statuses)
            for status_name in status_sequence:
                description = f"Статус заказа: {status_name}"
                is_terminal = status_name in ['Completed', 'Cancelled']
                values_list.append((order_id, description, status_name, is_terminal))

        try:
            query = 'INSERT INTO status (order_id, description, status_name, is_terminal) VALUES (%s, %s, %s, %s);'
            cursor.executemany(query, values_list)
            conn.commit()
            total_inserted += len(values_list)
            print(f"Вставлено {total_inserted} статусов")
        except Exception as e:
            conn.rollback()
            print(f"Ошибка при вставке статусов: {e}")

    print(f"Таблица 'status' заполнена {total_inserted} записями.")

def fill_promotion(product_ids):
    batch_size = 10000
    total_inserted = 0

    promotion_titles = [
        "Скидка на чистку ковров",
        "Акция на уборку после ремонта",
        "Специальное предложение на мытье окон",
        "Сезонная скидка на химчистку мебели",
        "Промо на уборку офисных помещений",
        "Скидка на услуги дезинфекции",
        "Предложение на уборку кухни",
        "Акция на чистку штор",
        "Скидка на полировку полов",
        "Специальное предложение на уборку после вечеринки",
        "Скидка на услуги по удалению пятен",
        "Акция на дезинфекцию помещений",
        "Сезонное предложение на уборку дачи",
        "Скидка на профессиональную мойку полов",
        "Специальное предложение на чистку матрасов"
    ]
    promotion_descriptions = [
        "Получите скидку 20% на чистку ковров.",
        "Сэкономьте на уборке после ремонта с нашей акцией.",
        "Скидка 15% на профессиональное мытье окон.",
        "Химчистка мебели со скидкой 25% только в этом месяце.",
        "Специальные цены на уборку офисов для новых клиентов.",
        "Бесплатная дезинфекция при заказе уборки квартиры.",
        "Скидка 10% на уборку кухни при первом заказе.",
        "Получите скидку на чистку штор при заказе от 3000 рублей.",
        "Скидка 30% на полировку полов в вашем доме.",
        "Бесплатная уборка после вечеринки при заказе услуг на сумму от 5000 рублей.",
        "Скидка 15% на услуги по удалению пятен с мебели.",
        "Специальное предложение на дезинфекцию офисных помещений.",
        "Сезонная скидка на уборку дачи и прилегающей территории.",
        "Скидка 20% на профессиональную мойку полов при первом заказе.",
        "Получите скидку на чистку матрасов при заказе других услуг."
    ]

    for batch_start in range(0, len(product_ids), batch_size):
        values_list = []
        batch_end = min(batch_start + batch_size, len(product_ids))
        for product_id in product_ids[batch_start:batch_end]:
            # Увеличиваем вероятность промоакций до 70%
            if random.random() < 0.7:
                title = random.choice(promotion_titles)
                description = random.choice(promotion_descriptions)
                start_date = fake.date_between(start_date='-1y', end_date='today')
                end_date = fake.date_between(start_date=start_date, end_date='+1y')
                discount = round(random.uniform(5.0, 50.0), 2)

                values_list.append((product_id, title, description, start_date, end_date, discount))

        if values_list:
            query = 'INSERT INTO promotion (product_id, title, description, start_date, end_date, discount) VALUES (%s, %s, %s, %s, %s, %s);'
            cursor.executemany(query, values_list)
            conn.commit()
            total_inserted += len(values_list)
            print(f"Вставлено {total_inserted} промоакций")

    print(f"Таблица 'promotion' заполнена {total_inserted} записями.")
    return

def fill_order_contains_services(order_ids, service_ids):
    batch_size = 10000
    total_inserted = 0

    for batch_start in range(0, len(order_ids), batch_size):
        values_list = []
        batch_end = min(batch_start + batch_size, len(order_ids))
        for order_id in order_ids[batch_start:batch_end]:
            num_services = random.randint(1, 10)
            services = random.sample(service_ids, min(num_services, len(service_ids)))
            for service_id in services:
                values_list.append((order_id, service_id))

        query = 'INSERT INTO order_contains_services (order_id, service_id) VALUES (%s, %s);'
        cursor.executemany(query, values_list)
        conn.commit()
        total_inserted += len(values_list)
        print(f"Вставлено {total_inserted} записей в order_contains_services")

    print(f"Таблица 'order_contains_services' заполнена {total_inserted} записями.")
    return

def fill_order_contains_products(order_ids, product_ids):
    batch_size = 10000
    total_inserted = 0

    for batch_start in range(0, len(order_ids), batch_size):
        values_list = []
        batch_end = min(batch_start + batch_size, len(order_ids))
        for order_id in order_ids[batch_start:batch_end]:
            num_products = random.randint(1, 10)
            products = random.sample(product_ids, min(num_products, len(product_ids)))
            for product_id in products:
                values_list.append((order_id, product_id))

        if values_list:
            query = 'INSERT INTO order_contains_products (order_id, product_id) VALUES (%s, %s);'
            cursor.executemany(query, values_list)
            conn.commit()
            total_inserted += len(values_list)
            print(f"Вставлено {total_inserted} записей в order_contains_products")

    print(f"Таблица 'order_contains_products' заполнена {total_inserted} записями.")
    return

def verify_data():
    cursor.execute('SELECT COUNT(*) FROM orders')
    total_orders = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM address')
    total_addresses = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(DISTINCT order_id) FROM address')
    unique_order_addresses = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(DISTINCT order_id) FROM status')
    unique_order_statuses = cursor.fetchone()[0]

    print(f"Всего заказов: {total_orders}")
    print(f"Всего адресов: {total_addresses}")
    print(f"Уникальных заказов с адресами: {unique_order_addresses}")
    print(f"Уникальных заказов со статусами: {unique_order_statuses}")

    if total_orders == unique_order_addresses == unique_order_statuses:
        print("Все заказы имеют адреса и статусы.")
    else:
        print("Некоторые заказы не имеют адресов или статусов.")

def main():
    try:
        # Очистка таблиц перед заполнением
        tables = ['order_contains_products', 'order_contains_services', 'promotion', 'status', 'review', 'user_have_addresses', 'address', 'orders', 'products', 'service', 'payment_method', 'employee', 'users']
        for table in tables:
            cursor.execute(f'TRUNCATE TABLE {table} CASCADE;')
            conn.commit()
            print(f"Таблица '{table}' очищена.")

        fill_users()
        fill_employee()
        fill_payment_method()
        fill_service()
        fill_products()

        cursor.execute('SELECT user_id FROM users')
        user_ids = [row[0] for row in cursor.fetchall()]
        cursor.execute('SELECT employee_id FROM employee')
        employee_ids = [row[0] for row in cursor.fetchall()]
        cursor.execute('SELECT payment_id FROM payment_method')
        payment_ids = [row[0] for row in cursor.fetchall()]
        cursor.execute('SELECT service_id FROM service')
        service_ids = [row[0] for row in cursor.fetchall()]
        cursor.execute('SELECT product_id FROM products')
        product_ids = [row[0] for row in cursor.fetchall()]

        # Проверяем, что списки не пусты
        if not user_ids:
            print("Список user_ids пуст.")
            return
        if not employee_ids:
            print("Список employee_ids пуст.")
            return
        if not payment_ids:
            print("Список payment_ids пуст.")
            return
            
        print(f"Примеры user_ids: {user_ids[:5]}")
        print(f"Примеры employee_ids: {employee_ids[:5]}")
        print(f"Примеры payment_ids: {payment_ids[:5]}")

        order_ids = fill_orders(user_ids, employee_ids, payment_ids)
        address_ids = fill_address(order_ids)
        fill_user_have_addresses(user_ids, address_ids)
        fill_review(user_ids, employee_ids)
        fill_status(order_ids)
        fill_promotion(product_ids)
        fill_order_contains_services(order_ids, service_ids)
        fill_order_contains_products(order_ids, product_ids)

        # Проверяем корректность данных
        verify_data()

    except (Exception, Error) as error:
        print("Ошибка при заполнении базы данных:", error)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")

if __name__ == "__main__":
    main()
