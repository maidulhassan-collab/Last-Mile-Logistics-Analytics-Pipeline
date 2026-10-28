-- Singular dbt data test.
-- A dbt data test passes when this query returns ZERO rows.

select *
from "logistics_intelligence"."dbt_dev_analytics"."mart_daily_kpi"
where
       delivery_success_rate_pct < 0
    or delivery_success_rate_pct > 100
    or sla_compliance_pct < 0
    or sla_compliance_pct > 100
    or avg_delivery_tat_hours < 0
    or total_orders < 0