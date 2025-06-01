import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta
import uuid
import json

NUM_PICKUP_POINTS = 1000
NUM_PRODUCTS = 100000
NUM_USERS = 50000
ORDERS_PER_USER = 1
LOGINS_PER_USER = 2
BALANCES_PER_USER = 1
DELIVERY_TIMES_PER_PRODUCT = 5

conn = psycopg2.connect(
    host="localhost",
    database="backend",
    user="backend",
    password="backend",
    port=15432
)
cur = conn.cursor()

fake = Faker()

def generate_pickup_points(n):
    return [
        (i, json.dumps({"street": fake.street_address(), "city": fake.city(), "zip": fake.postcode()}),
         f"POINT({random.uniform(-180, 180)} {random.uniform(-90, 90)})")
        for i in range(1, n + 1)
    ]

def generate_products(n):
    return [
        (i, round(random.uniform(10, 1000), 2), 
         round(random.uniform(0.1, 50), 2),
         fake.text(max_nb_chars=200), 
         ' '.join(fake.words(nb=2)).title(),
         round(random.uniform(0, 0.5), 2), 
         random.randint(1, 100))
        for i in range(1, n + 1)
    ]

def generate_users(n):
    return [
        (str(uuid.uuid4()), fake.first_name(), fake.last_name(), random.randint(18, 70), fake.email(),
         fake.date_time_between(start_date="-5y", end_date="now"), fake.password(length=12),
         random.choice([True, False]), random.choice([True, False]), random.choice([True, False]))
        for _ in range(n)
    ]

def insert_pickup_points(data):
    cur.executemany(
        "INSERT INTO pickup_points (pickup_id, address, location) VALUES (%s, %s, ST_GeographyFromText(%s))",
        data
    )
    conn.commit()

def insert_products(data):
    cur.executemany(
        "INSERT INTO products (product_id, price, weight, description, name, discount, amount) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        data
    )
    conn.commit()

def insert_users(data):
    cur.executemany(
        """INSERT INTO users (user_id, first_name, last_name, age, email, registration_dttm, password_hash, 
           is_active, is_superuser, is_verified) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        data
    )
    conn.commit()

def generate_user_credentials(user_ids):
    return [(uid, fake.password(length=12), True, False, False) for uid in user_ids]

def generate_tokens(user_ids):
    return [(uid, str(uuid.uuid4()), fake.date_time_between(start_date="+1d", end_date="+1y"), random.choice([True, False])) for uid in user_ids]

def generate_user_logins(user_ids, per_user):
    data = []
    for uid in user_ids:
        for _ in range(per_user):
            login_dttm = fake.date_time_between(start_date="-5y", end_date="now")
            data.append((
                uid, login_dttm, fake.ipv4_public(), fake.user_agent(),
                random.choice(["success", "failed"]),
                random.choice(["invalid password", "locked account", "network error"]) if random.random() < 0.2 else None
            ))
    return data

def generate_carts(user_ids, product_ids):
    return [(uid, random.sample(product_ids, random.randint(1, 20))) for uid in user_ids]

def generate_delivery_times(product_ids, pickup_ids, per_product):
    data = []
    for pid in product_ids:
        for pickup_id in random.sample(pickup_ids, per_product):
            data.append((
                pid, pickup_id, random.randint(24, 168),
                random.choice([True, False])
            ))
    return data

def generate_orders(user_ids, product_ids, pickup_ids):
    data = []
    for uid in user_ids:
        for _ in range(ORDERS_PER_USER):
            product_count = random.randint(1, 10)
            products = random.sample(product_ids, product_count)
            data.append((
                uid, products, [round(random.uniform(10, 1000), 2) for _ in products],
                fake.date_time_between(start_date="-3y", end_date="now"),
                random.choice(pickup_ids), random.choice(["standard", "express", "pickup"])
            ))
    return data

def generate_user_favorites(user_ids, product_ids):
    return [(uid, random.sample(product_ids, random.randint(1, 20))) for uid in user_ids]

def generate_premium_users(user_ids, probability=0.3):
    return [(uid, random.randint(5, 30)) for uid in user_ids if random.random() < probability]

def generate_user_balances(user_ids, per_user):
    data = []
    for uid in user_ids:
        start_date = fake.date_time_between(start_date="-2y", end_date="now")
        for _ in range(per_user):
            valid_from = start_date + timedelta(days=random.randint(1, 30))
            data.append((
                uid, round(random.uniform(0, 10000), 2), 
                valid_from,
                valid_from + timedelta(days=365)
            ))
    return data

def generate_user_payments(user_ids):
    return [(uid, fake.date_time_between(start_date="-2y", end_date="now"), round(random.uniform(10, 500), 2)) for uid in user_ids]

try:
    print("Генерация pickup_points...")
    pickup_points_data = generate_pickup_points(NUM_PICKUP_POINTS)
    print("Вставка pickup_points...")
    insert_pickup_points(pickup_points_data)
    pickup_ids = [row[0] for row in pickup_points_data]

    print("Генерация продуктов...")
    products_data = generate_products(NUM_PRODUCTS)
    print("Вставка продуктов...")
    insert_products(products_data)
    product_ids = [row[0] for row in products_data]

    print("Генерация пользователей...")
    users_data = generate_users(NUM_USERS)
    print("Вставка пользователей...")
    insert_users(users_data)
    user_ids = [row[0] for row in users_data]

    print("Вставка user_credentials...")
    cur.executemany("""INSERT INTO user_credentials (user_id, password_hash, is_active, is_superuser, is_verified) 
                    VALUES (%s, %s, %s, %s, %s)""", 
                    generate_user_credentials(user_ids))
    conn.commit()

    print("Вставка tokens...")
    cur.executemany("""INSERT INTO tokens (user_id, token_hash, expiry_date, revoked) 
                    VALUES (%s, %s, %s, %s)""", 
                    generate_tokens(user_ids))
    conn.commit()

    print("Вставка user_logins...")
    cur.executemany("""INSERT INTO user_logins (user_id, login_dttm, ip_address, user_agent, login_status, failure_reason) 
                    VALUES (%s, %s, %s, %s, %s, %s)""", 
                    generate_user_logins(user_ids, LOGINS_PER_USER))
    conn.commit()

    print("Вставка carts...")
    cur.executemany("""INSERT INTO carts (user_id, product_ids) 
                    VALUES (%s, %s)""", 
                    generate_carts(user_ids, product_ids))
    conn.commit()

    print("Вставка delivery_times...")
    cur.executemany("""INSERT INTO delivery_times (product_id, pickup_id, delivery_hours, is_express) 
                    VALUES (%s, %s, %s, %s)""", 
                    generate_delivery_times(product_ids, pickup_ids, DELIVERY_TIMES_PER_PRODUCT))
    conn.commit()

    print("Вставка orders...")
    cur.executemany("""INSERT INTO orders (user_id, product_ids, product_costs, order_dttm, pickup_id, order_type) 
                    VALUES (%s, %s, %s, %s, %s, %s)""", 
                    generate_orders(user_ids, product_ids, pickup_ids))
    conn.commit()

    print("Вставка user_favorites...")
    cur.executemany("""INSERT INTO user_favorites (user_id, favorites_ids) 
                    VALUES (%s, %s)""", 
                    generate_user_favorites(user_ids, product_ids))
    conn.commit()

    print("Вставка premium_users...")
    cur.executemany("""INSERT INTO premium_users (user_id, personal_discount) 
                    VALUES (%s, %s)""", 
                    generate_premium_users(user_ids))
    conn.commit()

    print("Вставка user_balances...")
    cur.executemany("""INSERT INTO user_balances (user_id, balance, valid_from, valid_to) 
                    VALUES (%s, %s, %s, %s)""", 
                    generate_user_balances(user_ids, BALANCES_PER_USER))
    conn.commit()

    print("Вставка user_payments...")
    cur.executemany("""INSERT INTO user_payments (user_id, payment_dttm, payment_amount) 
                    VALUES (%s, %s, %s)""", 
                    generate_user_payments(user_ids))
    conn.commit()

    print("✅ Все данные успешно сгенерированы и загружены.")

except Exception as e:
    print(f"❌ Ошибка: {e}")
    conn.rollback()
finally:
    cur.close()
    conn.close()