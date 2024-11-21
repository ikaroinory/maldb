select count(*) as `Total Count`
from malware_info
where sha256 in (select sha256 from download_info);
