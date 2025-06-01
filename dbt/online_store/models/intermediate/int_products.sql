{{ config(materialized='table') }}

-- Склеиваем продукты и время доставки
SELECT
  product_id,
  name,
  description,
  price,
  discount,
  amount_left,
  weight
FROM {{ ref('stg_online_shop__products') }} 
