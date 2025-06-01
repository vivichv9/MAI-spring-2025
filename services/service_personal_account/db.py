import psycopg2
class Database:
    def __init__(self,params):
        self.params = params

    def get_cart(self,user_id):
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT product_ids FROM carts WHERE user_id = %s", (user_id,))
                return cursor.fetchall()
    def get_orders(self,user_id):
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM orders WHERE user_id = %s", (user_id,))
                return cursor.fetchall()
    def change_password(self,user_id,new_pass_hash):
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE user_credentials SET password_hash = %s WHERE user_id = %s", (new_pass_hash,user_id,))
                return cursor.rowcount
    def change_user_name(self,user_id,new_name):
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""UPDATE users SET first_name = %s WHERE user_id = %s""",(new_name,user_id,))
                return cursor.rowcount
    def change_user_surname(self,user_id,new_surname):
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""UPDATE users SET last_name = %s WHERE user_id = %s""",(new_surname,user_id,))
                return cursor.rowcount

    def change_user_email(self, user_id, new_email):
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""UPDATE users SET email = %s WHERE user_id = %s""", (new_email, user_id,))
                return cursor.rowcount
    def change_user_age(self, user_id, new_age):
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""UPDATE users SET age = %s WHERE user_id = %s""", (new_age, user_id,))
                return cursor.rowcount