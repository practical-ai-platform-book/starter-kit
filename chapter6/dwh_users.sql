select
    user_id
    , gender
    , parse_date("%Y年%m月%d日", birthdate) as birthdate
from
    `raw_k_and_r_chap6.users`
;
