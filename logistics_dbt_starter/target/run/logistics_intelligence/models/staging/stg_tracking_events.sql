
  create view "logistics_intelligence"."dbt_dev_staging"."stg_tracking_events__dbt_tmp"
    
    
  as (
    with source as (
    select *
    from "logistics_intelligence"."raw"."tracking_events"
),
ranked as (
    select
        event_id,
        order_id,
        event_time,
        initcap(trim(event_type)) as event_type,
        hub_id,
        courier_id,
        nullif(trim(failure_reason), '') as failure_reason,
        row_number() over (
            partition by order_id, initcap(trim(event_type)), event_time
            order by event_id
        ) as duplicate_rank
    from source
)
select
    event_id,
    order_id,
    event_time,
    event_type,
    hub_id,
    courier_id,
    failure_reason
from ranked
where duplicate_rank = 1
  );