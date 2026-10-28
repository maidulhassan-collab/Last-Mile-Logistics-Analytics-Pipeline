
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        final_status as value_field,
        count(*) as n_records

    from "logistics_intelligence"."dbt_dev_analytics"."fct_orders"
    group by final_status

)

select *
from all_values
where value_field not in (
    'Delivered','Returned','Failed','Cancelled','In Transit','Out For Delivery'
)



  
  
      
    ) dbt_internal_test