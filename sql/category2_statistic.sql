select coalesce(category_second, 'unknown')             as `Threat Category 2`,
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
               max(case when rank = 2 then category end) as category_second
        from mtcr
        group by sha256
--         having category_first = 'trojan'
)
where sha256 in (select sha256 from download_info)
group by category_second;
