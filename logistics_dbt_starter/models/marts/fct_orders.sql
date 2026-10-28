with orders as (
    select *
    from {{ ref('stg_orders') }}
),
events as (
    select *
    from {{ ref('int_order_events') }}
)
select
    o.order_id,
    o.order_created_at,
    o.merchant_id,
    o.destination_city,
    o.destination_zone,
    o.service_type,
    o.payment_type,
    o.promised_delivery_date,
    o.final_status,
    e.latest_event_type,
    e.latest_event_time,
    e.delivered_at,
    e.failed_delivery_attempts,
    e.first_attempt_delivery_flag,
    case
        when e.delivered_at is null then null
        when e.delivered_at::date <= o.promised_delivery_date then 1
        else 0
    end as sla_compliant_flag,
    case
        when e.delivered_at is not null
        then round(extract(epoch from (e.delivered_at - o.order_created_at)) / 3600.0, 2)
        else null
    end as delivery_tat_hours,
    case when o.final_status = 'Delivered' then 1 else 0 end as delivered_flag,
    case when o.final_status = 'Returned' then 1 else 0 end as returned_flag,
    case when o.final_status = 'Failed' then 1 else 0 end as failed_flag,
    case when o.final_status = 'Cancelled' then 1 else 0 end as cancelled_flag
from orders o
left join events e on o.order_id = e.order_id
