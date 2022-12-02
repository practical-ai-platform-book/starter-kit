select
    purchased.date
    , purchased.user_id
    , purchased.item_id
    , canceled.transaction_id is not null as is_canceled
from
    `raw_k_and_r_chap6.transactions` as purchased
    left join `raw_k_and_r_chap6.transactions` as canceled
        on
            purchased.transaction_id = canceled.transaction_id
            and purchased.event_type = "purchase"
            and canceled.event_type = "cancel"
where
    purchased.event_type = "purchase"
    and purchased.date = @target_date
