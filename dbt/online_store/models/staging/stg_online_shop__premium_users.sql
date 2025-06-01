select 
    user_id,
    personal_discount
from {{ source('public','premium_users') }}
