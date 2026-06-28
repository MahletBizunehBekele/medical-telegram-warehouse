select

dense_rank() over(order by channel_name) as channel_key,

channel_name,

case

    when lower(channel_name) like '%lobelia%' then 'Cosmetics'

    when lower(channel_name) like '%pharma%' then 'Pharmaceutical'

    else 'Medical'

end as channel_type,

min(message_date) as first_post_date,

max(message_date) as last_post_date,

count(*) as total_posts,

avg(views) as avg_views

from {{ ref('stg_telegram_messages') }}

group by channel_name