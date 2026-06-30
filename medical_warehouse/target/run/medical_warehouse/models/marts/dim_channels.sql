
  
    

  create  table "medical_warehouse"."analytics"."dim_channels__dbt_tmp"
  
  
    as
  
  (
    SELECT

    ROW_NUMBER() OVER (
        ORDER BY channel_name
    ) AS channel_key,

    channel_name,

    CASE

        WHEN LOWER(channel_name) LIKE '%pharma%'
            THEN 'Pharmaceutical'

        WHEN LOWER(channel_name) LIKE '%cosmetic%'
            THEN 'Cosmetics'

        ELSE 'Medical'

    END AS channel_type,

    MIN(message_date) AS first_post_date,

    MAX(message_date) AS last_post_date,

    COUNT(*) AS total_posts,

    AVG(views) AS avg_views

FROM "medical_warehouse"."analytics"."stg_telegram_messages"

GROUP BY channel_name
  );
  