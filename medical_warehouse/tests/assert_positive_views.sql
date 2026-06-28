select *

from {{ ref('fct_messages') }}

where views < 0