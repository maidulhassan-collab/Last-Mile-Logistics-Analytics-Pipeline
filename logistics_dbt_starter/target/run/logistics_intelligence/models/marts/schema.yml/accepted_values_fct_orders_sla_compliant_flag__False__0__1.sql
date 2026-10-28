
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        sla_compliant_flag as value_field,
        count(*) as n_records

    from "logistics_intelligence"."dbt_dev_analytics"."fct_orders"
    group by sla_compliant_flag

)

select *
from all_values
where value_field not in (
    0,1
)



  
  
      
    ) dbt_internal_test