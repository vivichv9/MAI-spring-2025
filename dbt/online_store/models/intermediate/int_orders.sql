{{ config(
    materialized='incremental',
    unique_key=['order_id','product_id']
) }}

-- Разворачиваем массивы product_ids и product_costs
WITH exploded AS (
  SELECT
    o.order_id,
    o.user_id,
    o.order_dt,
    o.order_type,
    t.product_id,
    t.product_cost
  FROM {{ ref('stg_online_shop__orders') }} AS o
  CROSS JOIN UNNEST(o.product_ids, o.product_costs) AS t(product_id, product_cost)
)

SELECT
  order_id,
  user_id,
  product_id,
  product_cost      AS revenue,
  order_dt,
  order_type
FROM exploded

{% if is_incremental() %}
  -- Загружаем только новые дни
  WHERE order_dt >= (SELECT MAX(order_dt) FROM {{ this }})
{% endif %}
