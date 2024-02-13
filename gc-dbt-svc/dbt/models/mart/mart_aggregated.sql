with mart_agg AS (

    SELECT
        *
    FROM
        {{ ref('int_crm') }}

),

won_opp AS (

    SELECT
        SUM(opportunity_value) AS won_amount_total,
        COUNT(opportunity_id) AS won_opportunities_cnt
    FROM
        mart_agg
    GROUP BY milestone_name
    HAVING milestone_name = 'Won'

),

oppurtunities AS (

    SELECT
        COUNT(opportunity_id) AS total_opportunities_cnt
    FROM
        mart_agg

)

SELECT
    oppurtunities.total_opportunities_cnt,
    won_opp.*
FROM
    won_opp
CROSS JOIN
    oppurtunities
