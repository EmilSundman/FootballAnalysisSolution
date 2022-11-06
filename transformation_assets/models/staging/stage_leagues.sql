with source as (

  select * from {{ source('raw', 'leagues') }}

),

renamed as (

  select distinct 
    cast(id as int) as league_id,
    cast(name as varchar) as league_name,
    cast(type as varchar) as league_type,
    cast(logomedia as varchar) as league_logo_media,
    cast(country as varchar) as league_country,
    cast(countrycode as varchar) as league_country_code,
    cast(countryflagmedia as varchar) as league_country_flag_media

  from source

)

select * from renamed
