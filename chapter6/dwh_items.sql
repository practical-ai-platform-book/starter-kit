select
    item_id
    , if(trim(category) = "", null, category) as category
from
    `raw_k_and_r_chap6.items`
;
