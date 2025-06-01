import psycopg2
class Database:
    def __init__(self,params):
        self.params = params
    def get_orders(self,user_id):
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM orders WHERE user_id = %s", (user_id,))
                return cursor.fetchall()
    def create_order(self,user_id,product_ids,product_costs,order_dttm,pickup_id,order_type):
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO orders (user_id, product_ids, product_costs, order_dttm, pickup_id, order_type)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING order_id;
                    """,
                    (user_id, product_ids, product_costs, order_dttm, pickup_id, order_type)
                )
                order_id = cursor.fetchone()[0]
                return order_id
    def cancel_order(self,order_id):
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""UPDATE orders SET order_type = 'canceled' WHERE order_id = %s""",(order_id,))
                return cursor.rowcount
    def get_user_orders(self,user_id):
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""SELECT * FROM orders WHERE user_id = %s""",(user_id,))
                return cursor.fetchall()
    def get_order(self,order_id):
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""SELECT * FROM orders WHERE order_id = %s""",(order_id,))
                return cursor.fetchone()