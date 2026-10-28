
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select merchant_id
from "logistics_intelligence"."dbt_dev_analytics"."fct_orders"
where merchant_id is null



  
  
      
    ) dbt_internal_test