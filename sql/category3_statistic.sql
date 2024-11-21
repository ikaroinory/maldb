select coalesce(category_third, 'unknown')             as `Threat Category 3`,
       count(*)                                         as `Count`,
       round(count(*) * 1.0 / sum(count(*)) over (), 4) as `Percentage`
from (
        with mtcr as (
            with mtc as (
                select distinct *
                from malware_threat_category
                where sha256 in (select sha256 from malware_info)
            )
            select *,
                 row_number() over (partition by sha256 order by count desc, category desc) as rank
            from mtc
        )
        select sha256,
               max(case when rank = 3 then category end) as category_third
        from mtcr
        group by sha256
)
where sha256 in (select sha256 from download_info)
group by category_third;
