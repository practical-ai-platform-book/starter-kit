with
    /* 商品別の売上（うちキャンセルされていないもの）個数を集計する */
    item_purchase_counts as (
        select
            purchased.item_id
            , count(*) as cnt
        from
            `raw_k_and_r_chap6.transactions` as purchased
            /*
            transactionsには購入とキャンセルの二種類のイベントが含まれている
            transaction_idで自己結合し，キャンセルされていない売り上げを調べる
            */
            left join `raw_k_and_r_chap6.transactions` as canceled
                on
                    purchased.transaction_id = canceled.transaction_id
                    and purchased.event_type = "purchase"
                    and canceled.event_type = "cancel"
        where
            purchased.date between "2021-01-01" and "2021-02-01"
            and purchased.event_type = "purchase"
            and canceled.transaction_id is null
        group by
            item_id
    )
select
    category
    , array_agg(item_id order by cnt desc limit 10) as top_items
from
    item_purchase_counts
    inner join `raw_k_and_r_chap6.items` using(item_id)
/*
    カテゴリ名が空白になっている場合は集計に含めない
 */
where
    trim(category) != ""
group by
    category
order by
    1
;
