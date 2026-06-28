select distinct

cast(to_char(message_date,'YYYYMMDD') as integer) as date_key,

cast(message_date as date) as full_date,

extract(dow from message_date) as day_of_week,

to_char(message_date,'Day') as day_name,

extract(week from message_date) as week_of_year,

extract(month from message_date) as month,

to_char(message_date,'Month') as month_name,

extract(quarter from message_date) as quarter,

extract(year from message_date) as year,

case

when extract(dow from message_date) in (0,6)

then true

else false

end as is_weekend

from {{ ref('stg_telegram_messages') }}