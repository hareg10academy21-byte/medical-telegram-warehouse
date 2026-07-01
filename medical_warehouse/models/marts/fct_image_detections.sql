SELECT
    f.message_id,
    f.channel_key,
    f.date_key,

    d.detected_class,
    d.confidence_score,
    d.image_category

FROM raw.image_detections d

JOIN {{ ref('fct_messages') }} f
ON d.message_id = f.message_id