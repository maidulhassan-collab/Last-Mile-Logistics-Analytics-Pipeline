
    
    

select
    order_date as unique_field,
    count(*) as n_records

from "logistics_intelligence"."dbt_dev_analytics"."mart_daily_kpi"
where order_date is not null
group by order_date
having count(*) > 1


