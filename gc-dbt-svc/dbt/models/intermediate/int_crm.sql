WITH int_data as (

    SELECT
        _pk,
        ROW_NUMBER() OVER (PARTITION BY party_id, opportunity_id ORDER BY updated_at DESC) AS rn,
        opportunity_id,
        party_id,
        party_name,
        first_name,
        last_name,
        opportunity_name,
        CAST(value_amount AS INT64) as value_amount, 
        CAST(duration AS INT64) as duration,
        duration_basis,
        milestone_name,
        updated_at

    FROM
        {{ ref('stg_crm') }}
),

final AS (

    SELECT
        * EXCEPT (rn),
        COALESCE(value_amount * duration, value_amount) as opportunity_value,
        COALESCE(party_name, CONCAT(first_name, ' ', last_name)) AS client
    FROM
        int_data
    WHERE rn = 1
)

SELECT 
    * 
FROM 
    final