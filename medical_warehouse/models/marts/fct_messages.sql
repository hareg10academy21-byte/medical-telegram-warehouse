SELECT

    s.message_id,

    c.channel_key,

    d.date_key,

    s.message_text,

    s.message_length,

    s.views,

    s.forwards,

    s.has_image

FROM {{ ref('stg_telegram_messages') }} s

LEFT JOIN {{ ref('dim_channels') }} c
    ON s.channel_name = c.channel_name

LEFT JOIN {{ ref('dim_dates') }} d
    ON s.message_date::DATE = d.full_date