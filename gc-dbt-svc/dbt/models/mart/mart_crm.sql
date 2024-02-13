WITH mart_data AS(

    SELECT
        _pk,
        client,
        opportunity_name,
        opportunity_value,
        milestone_name
    FROM
        {{ ref('int_crm') }}

)

SELECT
    *
FROM
    mart_data

