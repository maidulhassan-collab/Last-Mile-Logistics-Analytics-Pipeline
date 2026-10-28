
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select order_date
from "logistics_intelligence"."dbt_dev_analytics"."mart_daily_kpi"
where order_date is null



  
  
      
    ) dbt_internal_test