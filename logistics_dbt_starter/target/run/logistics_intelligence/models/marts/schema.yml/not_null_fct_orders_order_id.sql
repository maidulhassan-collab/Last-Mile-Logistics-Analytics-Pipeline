
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select order_id
from "logistics_intelligence"."dbt_dev_analytics"."fct_orders"
where order_id is null



  
  
      
    ) dbt_internal_test