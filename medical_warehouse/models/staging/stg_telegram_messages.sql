with source as (

    select * from raw.telegram_messages

)

select

    message_id,
    channel_name,
    cast(message_date as timestamp) as message_date,
    trim(message_text) as message_text,
    coalesce(views,0) as views,
    coalesce(forwards,0) as forwards,
    has_media,
    image_path,

    length(coalesce(message_text,'')) as message_length,

    case
        when image_path is null then false
        else true
    end as has_image

from source

where message_id is not null