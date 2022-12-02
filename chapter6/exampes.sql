select
    user_gender
    , count(*)
from
    `k_and_r.transactions_combined`
where
    not is_canceled /* キャンセルされていない購入記録のみ */
group by
    1
;

select
    item_category
    , countif(is_canceled) / count(*)
from
    `k_and_r.transactions_combined`
/* is_canceled で条件づけられていないことに注意 */
group by
    1
;

