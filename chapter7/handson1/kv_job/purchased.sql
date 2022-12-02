/*
ユーザ，アイテムごとに直近の購入日を取得する
*/
create temp table transactions as
    select
        user_id
        , item_id
        , first_value(date)
            over (partition by user_id, item_id order by date desc)
            as date_last_purchased
    from
        `k_and_r.transactions`
    where
        date <= @target_date
;

/*
ユーザごとに直近N件の購入アイテムを抽出する
*/
select
    user_id
    , array_agg(item_id order by date_last_purchased desc limit @max_items)
        as item_ids
from
    transactions
group by
    user_id
;
