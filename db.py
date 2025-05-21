import psycopg2
class Database:
    def __init__(self,params):
        self.params = params

    def get_cart(self,user_id):
        with psycopg2.connect(self.params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT product_id FROM cart WHERE user_id = %s", (user_id,))
                return cursor.fetchall()
    def get_purchases(self,user_id):
        with psycopg2.connect(self.params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT product_id FROM purchases WHERE user_id = %s", (user_id,))
                return cursor.fetchall()