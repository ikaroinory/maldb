create table if not exists malware_info (
    sha256                           text primary key,
    sha1                             text unique,
    md5                              text unique,
    tlsh                             text,
    permhash                         text,

    name                             text,
    type                             text,
    size                             integer,

    threat_category                  text,
    threat_name                      text,
    threat_label                     text,

    first_submission_date_virustotal datetime,
    last_submission_date_virustotal  datetime,
    last_analysis_date_virustotal    datetime,

    source                           text not null
);

create table if not exists malware_tag (
    sha256 text not null,
    tag    text not null,

    constraint malware_tag_sha256_tag_unique
        unique (sha256, tag)
);

create table if not exists malware_type (
    sha256 text not null,
    type   text not null,

    constraint malware_type_sha256_type_unique
        unique (sha256, type)
);

create table if not exists malware_threat_name (
    sha256 text not null,
    name   text    not null,
    count  integer not null
);

create table if not exists malware_threat_category (
    sha256   text not null,
    category text    not null,
    count    integer not null
);

create table if not exists download_info (
    sha256        text primary key,
    download_time datetime,
    file_path     text,
    source        text not null
);

create table if not exists not_found_info (
    sha256 text primary key,
    source text not null,

    constraint not_found_info_sha256_source_unique
        unique (sha256, source)
);
