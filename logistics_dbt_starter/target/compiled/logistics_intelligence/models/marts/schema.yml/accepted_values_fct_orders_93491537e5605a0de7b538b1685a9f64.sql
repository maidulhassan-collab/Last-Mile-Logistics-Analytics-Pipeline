
    
    

with all_values as (

    select
        first_attempt_delivery_flag as value_field,
        count(*) as n_records

    from "logistics_intelligence"."dbt_dev_analytics"."fct_orders"
    group by first_attempt_delivery_flag

)

select *
from all_values
where value_field not in (
    0,1
)


