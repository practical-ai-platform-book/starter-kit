with
    purchase_counts as (
        select
            item_category
            , item_id
            , count(*) as cnt
        from
            `k_and_r.transactions_combined`
        where
            not is_canceled
        group by
            item_category
            , item_id
    )
select
    item_category as category
    , array_agg(item_id order by cnt desc limit 10) as top_items
from
    purchase_counts
group by
    item_category
;
