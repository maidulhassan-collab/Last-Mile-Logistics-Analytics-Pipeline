with source as (
    select *
    from "logistics_intelligence"."raw"."orders"
),
cleaned as (
    select
        order_id,
        merchant_id,
        order_created_at,
        origin_hub_id,
        destination_hub_id,
        initcap(trim(destination_city)) as destination_city,
        initcap(trim(destination_zone)) as destination_zone,
        initcap(trim(service_type)) as service_type,
        initcap(trim(package_category)) as package_category,
        weight_kg,
        declared_value_bdt,
        shipping_fee_bdt,
        upper(trim(payment_type)) as payment_type,
        cod_amount_bdt,
        promised_delivery_date,
        assigned_courier_id,
        initcap(trim(final_status)) as final_status,
        trim(order_source) as order_source,
        case when weight_kg is null then 1 else 0 end as dq_missing_weight,
        case when promised_delivery_date < order_created_at::date then 1 else 0 end as dq_invalid_promised_date
    from source
)
select *
from cleaned