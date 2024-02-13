WITH source AS (
    SELECT 
    {{ dbt_utils.generate_surrogate_key([
    'topic', '`partition`', 'offset'
    ]) }} AS _pk,
    * 
    FROM {{ source('crm_staging', 'crm_raw') }}
),

value_data AS (
    SELECT
        _pk,
        JSON_EXTRACT_SCALAR(source.value, '$.event') AS event,
        JSON_EXTRACT(source.value, '$.payload') AS payload,
    FROM
        source
),

final AS (

    SELECT
        _pk,
        event,
        JSON_EXTRACT_SCALAR(payload, '$[0].id') AS opportunity_id,
        JSON_EXTRACT_SCALAR(payload, '$[0].owner.id') AS owner_id,
        JSON_EXTRACT_SCALAR(payload, '$[0].owner.deleted') AS owner_deleted,
        JSON_EXTRACT_SCALAR(payload, '$[0].owner.username') AS owner_username,
        JSON_EXTRACT_SCALAR(payload, '$[0].owner.pictureURL') AS owner_pictureURL,
        JSON_EXTRACT_SCALAR(payload, '$[0].owner.name') AS owner_name,
        JSON_EXTRACT_SCALAR(payload, '$[0].team') AS team,
        CAST(JSON_EXTRACT_SCALAR(payload, '$[0].lastStageChangedAt') AS TIMESTAMP) AS last_stage_changed_at,
        JSON_EXTRACT_SCALAR(payload, '$[0].party.id') AS party_id,
        JSON_EXTRACT_SCALAR(payload, '$[0].party.type') AS party_type,
        JSON_EXTRACT_SCALAR(payload, '$[0].party.name') AS party_name,
        JSON_EXTRACT_SCALAR(payload, '$[0].party.firstName') AS first_name,
        JSON_EXTRACT_SCALAR(payload, '$[0].party.lastName') AS last_name,                
        JSON_EXTRACT_SCALAR(payload, '$[0].party.pictureURL') AS party_pictureURL,
        JSON_EXTRACT_SCALAR(payload, '$[0].lostReason') AS lost_reason,
        CAST(JSON_EXTRACT_SCALAR(payload, '$[0].createdAt') AS TIMESTAMP) AS created_at,
        CAST(JSON_EXTRACT_SCALAR(payload, '$[0].updatedAt') AS TIMESTAMP) AS updated_at,
        JSON_EXTRACT_SCALAR(payload, '$[0].name') AS opportunity_name,
        JSON_EXTRACT_SCALAR(payload, '$[0].value.amount') AS value_amount,
        JSON_EXTRACT_SCALAR(payload, '$[0].value.currency') AS value_currency,
        JSON_EXTRACT_SCALAR(payload, '$[0].duration') AS duration,
        JSON_EXTRACT_SCALAR(payload, '$[0].durationBasis') AS duration_basis,
        JSON_EXTRACT_SCALAR(payload, '$[0].milestone.id') AS milestone_id,
        JSON_EXTRACT_SCALAR(payload, '$[0].milestone.name') AS milestone_name,
        JSON_EXTRACT_SCALAR(payload, '$[0].lastOpenMilestone.id') AS last_open_milestone_id,
        JSON_EXTRACT_SCALAR(payload, '$[0].lastOpenMilestone.name') AS last_open_milestone_name,
        JSON_EXTRACT_SCALAR(payload, '$[0].probability') AS probability,
        CAST(JSON_EXTRACT_SCALAR(payload, '$[0].expectedCloseOn') AS TIMESTAMP) AS expected_close_on,
        CAST(JSON_EXTRACT_SCALAR(payload, '$[0].closedOn') AS TIMESTAMP) AS closed_on,
        JSON_EXTRACT_SCALAR(payload, '$[0].description') AS description,
        CAST(JSON_EXTRACT_SCALAR(payload, '$[0].lastContactedAt') AS TIMESTAMP) AS last_contacted_at
    FROM
        value_data

)

SELECT
    *
FROM
    final