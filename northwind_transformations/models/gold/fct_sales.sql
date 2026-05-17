
with orders as (
    select * from {{ ref('stg_orders') }}
),
details as (
    select 
        order_id,
        sum(total_price) as order_total_value,
        sum(quantity) as total_items
    from {{ ref('stg_order_details') }}
    group by order_id
)

select
    o.order_id,
    o.customer_id,
    o.order_date,
    o.ship_country,
    d.order_total_value,
    d.total_items
from orders o
left join details d on o.order_id = d.order_id
