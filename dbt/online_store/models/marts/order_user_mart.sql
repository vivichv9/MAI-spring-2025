{{ 
  config(
    materialized='table',
    schema='marts'
  )
}}

-- Витрина: информация о каждом заказе плюс данные о пользователе
SELECT
  o.order_id,
  o.user_id,
  u.first_name,
  u.last_name,
  u.personal_discount,
  u.premium_flg,
  o.product_id,
  o.revenue,
  o.order_dt     AS order_date,
  o.order_type
FROM {{ ref('int_orders') }} AS o
JOIN {{ ref('int_users') }}  AS u
  ON o.user_id = u.user_id
