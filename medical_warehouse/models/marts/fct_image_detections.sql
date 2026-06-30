select

    d.message_id,

    f.channel_key,

    f.date_key,

    d.detected_class,

    d.confidence_score,

    d.image_category

from raw.image_detections d

join {{ ref('fct_messages') }} f
    on d.message_id = f.message_id

join {{ ref('dim_channels') }} c
    on f.channel_key = c.channel_key
   and d.channel_name = c.channel_name