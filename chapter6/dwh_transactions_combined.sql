select
    item_id
    , user_id
    , date
    , is_canceled
    , gender as user_gender
    , birthdate as user_birthdate
    , category as item_category
from
    `k_and_r.transactions` transactions
    left join `k_and_r.users` using(user_id)
    left join `k_and_r.items` using(item_id)
where
    date = @target_date
;
