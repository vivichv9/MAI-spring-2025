import psycopg2
class Database:
    def __init__(self,params):
        self.params = params

    def get_cart(self,user_id):
        with psycopg2.connect(self.params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT product_ids FROM carts WHERE user_id = %s", (user_id,))
                return cursor.fetchall()
    def get_orders(self,user_id):
        with psycopg2.connect(self.params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM orders WHERE user_id = %s", (user_id,))
                return cursor.fetchall()
    def change_password(self,user_id,new_pass_hash):
        with psycopg2.connect(self.params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE user_credentials SET password_hash = %s WHERE user_id = %s", (new_pass_hash,user_id,))
                return cursor.fetchall()