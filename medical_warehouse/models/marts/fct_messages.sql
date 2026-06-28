select

s.message_id,

c.channel_key,

d.date_key,

s.message_text,

s.message_length,

s.views,

s.forwards,

s.has_image

from {{ ref('stg_telegram_messages') }} s

join {{ ref('dim_channels') }} c

using(channel_name)

join {{ ref('dim_dates') }} d

on cast(s.message_date as date)=d.full_date