select coalesce(threat_name, 'unknown')                 as `Threat Name`,
       count(*)                                         as `Count`,
       round(count(*) * 1.0 / sum(count(*)) over (), 4) as `Percentage`
from malware_info
where sha256 in (select sha256 from download_info)
group by threat_name;
