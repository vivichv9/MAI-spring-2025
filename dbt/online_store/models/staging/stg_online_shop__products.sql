select 
    product_id,
    price,
    weight,
    description,
    name,
    discount,
    amount as amount_left
from {{ source('public','products') }}
