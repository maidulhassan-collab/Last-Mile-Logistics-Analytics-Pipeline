
  create view "logistics_intelligence"."dbt_dev_intermediate"."int_order_events__dbt_tmp"
    
    
  as (
    with events as (
    select *
    from "logistics_intelligence"."dbt_dev_staging"."stg_tracking_events"
),
latest_event as (
    select
        order_id,
        event_type as latest_event_type,
        event_time as latest_event_time,
        row_number() over (
            partition by order_id
            order by event_time desc, event_id desc
        ) as rn
    from events
),
event_summary as (
    select
        order_id,
        max(event_time) filter (where event_type = 'Delivered') as delivered_at,
        count(*) filter (where event_type = 'Out For Delivery') as out_for_delivery_attempts,
        count(*) filter (where event_type = 'Delivery Attempt Failed') as failed_delivery_attempts
    from events
    group by order_id
)
select
    e.order_id,
    e.delivered_at,
    e.out_for_delivery_attempts,
    e.failed_delivery_attempts,
    case
        when e.delivered_at is not null and e.failed_delivery_attempts = 0 then 1
        when e.delivered_at is not null then 0
        else null
    end as first_attempt_delivery_flag,
    l.latest_event_type,
    l.latest_event_time
from event_summary e
left join latest_event l
    on e.order_id = l.order_id
   and l.rn = 1
  );