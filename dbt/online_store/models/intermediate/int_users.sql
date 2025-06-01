{{ config(materialized='table') }}

-- Объединяем базовых пользователей и премиум-скидки
select
    u.user_id,
    u.first_name,
    u.last_name,
    u.age,
    u.created_dt,
    coalesce(pu.personal_discount, 0) AS personal_discount,
    case 
      when pu.user_id is not null then 1
      else 0
    end as premium_flg
from {{ ref('stg_online_shop__users') }} as u
    left join{{ ref('stg_online_shop__premium_users') }} as pu
        on u.user_id = pu.user_id
