select 
    user_id,
    first_name,
    last_name,
    age,
    registration_dttm::date as created_dt
from {{ source('public','users') }}
