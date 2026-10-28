with orders as (
    select *
    from {{ ref('fct_orders') }}
)
select
    order_created_at::date as order_date,
    count(*) as total_orders,
    sum(delivered_flag) as delivered_orders,
    sum(returned_flag) as returned_orders,
    round(
        100.0 * sum(delivered_flag)
        / nullif(count(*) filter (where final_status <> 'Cancelled'), 0),
        2
    ) as delivery_success_rate_pct,
    round(
        100.0 * sum(sla_compliant_flag)
        / nullif(count(sla_compliant_flag), 0),
        2
    ) as sla_compliance_pct,
    round(
        avg(delivery_tat_hours) filter (where delivered_flag = 1),
        2
    ) as avg_delivery_tat_hours
from orders
group by order_created_at::date
