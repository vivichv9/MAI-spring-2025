select 
    order_id,
    user_id,
    product_ids,
    product_costs,
    order_dttm::date as order_dt,
    order_type
from {{ source('public','orders') }}
