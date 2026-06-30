
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  SELECT *
FROM "medical_warehouse"."analytics"."stg_telegram_messages"
WHERE views < 0
  
  
      
    ) dbt_internal_test