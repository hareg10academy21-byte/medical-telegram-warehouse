
  create view "medical_warehouse"."analytics"."stg_telegram_messages__dbt_tmp"
    
    
  as (
    SELECT

    message_id,

    channel_name,

    CAST(message_date AS TIMESTAMP) AS message_date,

    TRIM(message_text) AS message_text,

    COALESCE(views,0) AS views,

    COALESCE(forwards,0) AS forwards,

    has_image,

    image_path,

    LENGTH(
        COALESCE(message_text,'')
    ) AS message_length

FROM "medical_warehouse"."raw"."telegram_messages"

WHERE message_text IS NOT NULL
  );