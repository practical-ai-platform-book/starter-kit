/*
まずはアイテムごとの購入件数をカウントする
*/
with
    item_counts as (
        select
            item_id
            , count(*) as cnt
        from
            `k_and_r.transactions`
        where
            date = @target_date
        group by
            item_id
    )

/*
カテゴリごとに，購入件数の多い順に10件のアイテムを抽出する
*/
select
    category
    , array_agg(item_id order by cnt desc limit 10) as items
from
    item_counts
    inner join `k_and_r.items`
        using(item_id)
group by
    category
;
