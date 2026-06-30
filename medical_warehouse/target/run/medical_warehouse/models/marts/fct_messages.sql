
  
    

  create  table "medical_warehouse"."analytics"."fct_messages__dbt_tmp"
  
  
    as
  
  (
    SELECT

    s.message_id,

    c.channel_key,

    TO_CHAR(
        s.message_date,
        'YYYYMMDD'
    )::INTEGER
        AS date_key,

    s.message_text,

    s.message_length,

    s.views,

    s.forwards,

    s.has_image

FROM "medical_warehouse"."analytics"."stg_telegram_messages" s

JOIN "medical_warehouse"."analytics"."dim_channels" c

ON s.channel_name = c.channel_name
  );
  