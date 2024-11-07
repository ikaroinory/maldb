import sqlite3
from pathlib import Path

import pandas as pd
from openpyxl.styles import Alignment, Border, Font, Side
from openpyxl.utils import get_column_letter

from path import get_export_path

# malware_info_sql = '''
#     select sha256                           as SHA256,
#            sha1                             as SHA1,
#            md5                              as MD5,
#            tlsh                             as TLSH,
#            permhash                         as Permhash,
#            name                             as `Sample Name`,
#            type                             as `Sample Type`,
#            size                             as `Sample Size`,
#            threat_category                  as `Threat Category`,
#            threat_name                      as `Threat Name`,
#            threat_label                     as `Threat Label`,
#            first_submission_date_VirusTotal as `First Submission Date (VirusTotal)`,
#            last_submission_date_VirusTotal  as `Last Submission Date (VirusTotal)`,
#            last_analysis_date_VirusTotal    as `Last Analysis Date (VirusTotal)`,
#            source                           as `Sample Source`
#     from malware_info
#     where sha256 in (select sha256 from download_info);
# '''
malware_info_sql = '''
    select malware_info.sha256              as `SHA256`,
           sha1                             as `SHA1`,
           md5                              as `MD5`,
           tlsh                             as `TLSH`,
           permhash                         as `Permhash`,
           name                             as `Sample Name`,
           type                             as `Sample Type`,
           size                             as `Sample Size`,
           threat_category                  as `Threat Category`,
           category_second                  as `Threat Category 2`,
           threat_name                      as `Threat Name`,
           threat_label                     as `Threat Label`,
           first_submission_date_virustotal as `First Submission Date (VirusTotal)`,
           last_submission_date_virustotal  as `Last Submission Date (VirusTotal)`,
           last_analysis_date_virustotal    as `Last Analysis Date (VirusTotal)`,
           source                           as `Sample Source`
    from malware_info,
         (with rankedcategories as (select mtc.sha256,
                                           mtc.category,
                                           mtc.count,
                                           rank() over (partition by mtc.sha256 order by mtc.count desc) as rank
                                    from malware_threat_category mtc
                                    where mtc.sha256 in (select sha256 from malware_info))
          select sha256,
                 max(case when rank = 2 then category end) as category_second
          from rankedcategories
          group by sha256) other
    where malware_info.sha256 == other.sha256
      and malware_info.sha256 in (select sha256 from download_info);
'''
total_count_sql = '''
    select count(*) as `Total Count`
    from malware_info
    where sha256 in (select sha256 from download_info);
'''
category_statistic_sql = '''
    select coalesce(threat_category, 'unknown')             as `Threat Category 2`,
           count(*)                                         as `Count`,
           round(count(*) * 1.0 / sum(count(*)) over (), 4) as `Percentage`
    from malware_info
    where sha256 in (select sha256 from download_info)
    group by threat_category;
'''
category2_statistic_sql = '''
    select coalesce(category_second, 'unknown')             as `Threat Category`,
           count(*)                                         as `Count`,
           round(count(*) * 1.0 / sum(count(*)) over (), 4) as `Percentage`
    from (with rankedcategories as (select mtc.sha256,
                                           mtc.category,
                                           mtc.count,
                                           rank() over (partition by mtc.sha256 order by mtc.count desc) as rank
                                    from malware_threat_category mtc
                                    where mtc.sha256 in (select sha256 from malware_info))
          select sha256,
                 max(case when rank = 1 then category end) as category_first,
                 max(case when rank = 2 then category end) as category_second
          from rankedcategories
          group by sha256
          having category_first = 'trojan')
    where sha256 in (select sha256 from download_info)
    group by category_second;
'''
name_statistic_sql = '''
    select coalesce(threat_name, 'unknown')                 as `Threat Name`,
           count(*)                                         as `Count`,
           round(count(*) * 1.0 / sum(count(*)) over (), 4) as `Percentage`
    from malware_info
    where sha256 in (select sha256 from download_info)
    group by threat_name;
'''


def export(db_path: str, path: str | None) -> None:
    if path is None:
        path = get_export_path()

    excel_path = Path(path) / 'export_info.maldb.xlsx'

    with sqlite3.connect(db_path) as conn:
        malware_info_df = pd.read_sql_query(malware_info_sql, conn)
        total_count_df = pd.read_sql_query(total_count_sql, conn)
        category_statistic_df = pd.read_sql_query(category_statistic_sql, conn)
        category2_statistic_df = pd.read_sql_query(category2_statistic_sql, conn)
        name_statistic_df = pd.read_sql_query(name_statistic_sql, conn)

    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        malware_info_df.to_excel(writer, sheet_name='Malware Samples Information', index=False)
        total_count_df.to_excel(writer, sheet_name='Statistic', index=False, startrow=1, startcol=1)
        category_statistic_df.to_excel(writer, sheet_name='Statistic', index=False, startrow=1, startcol=3)
        category_statistic_df.to_excel(writer, sheet_name='Statistic', index=False, startrow=1, startcol=3)
        category2_statistic_df.to_excel(writer, sheet_name='Statistic', index=False, startrow=1, startcol=7)
        name_statistic_df.to_excel(writer, sheet_name='Statistic', index=False, startrow=1, startcol=11)

        courier_new_font = Font(name='Courier New', size=12)
        courier_new_bold_font = Font(name='Courier New', size=12, bold=True)
        center_alignment = Alignment(horizontal='center', vertical='center')
        thin_side = Side(border_style="thin", color="000000")
        border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)

        wb = writer.book
        ws = wb['Malware Samples Information']

        ws.auto_filter.ref = f'A1:{get_column_letter(ws.max_column)}{ws.max_row}'

        column_index = 1
        for column in ws.columns:
            max_len = 0
            column_letter = column[0].column_letter
            for cell in column:
                cell.font = courier_new_font
                cell.border = border
                if cell.value:
                    max_len = max(max_len, len(str(cell.value)))

                if column_index in [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 13, 14, 15, 16]:
                    cell.alignment = center_alignment
            ws.column_dimensions[column_letter].width = max_len * 1.5
            column_index += 1

        for cell in ws[1]:
            cell.font = courier_new_bold_font
            cell.alignment = center_alignment

        ws = wb['Statistic']
        column_index = 1
        for column in ws.columns:
            max_len = 0
            column_letter = column[0].column_letter
            for cell in column:
                cell.font = courier_new_font
                if cell.value:
                    max_len = max(max_len, len(str(cell.value)))

            ws.column_dimensions[column_letter].width = max_len * 1.5
            column_index += 1

        ws['B3'].alignment = center_alignment

        for column in ws.columns:
            for cell in column:
                if cell.value:
                    cell.border = border
        for cell in ws[2]:
            cell.font = courier_new_bold_font
            cell.alignment = center_alignment

        for cell in ws['F']:
            cell.number_format = '0.00%'
        for cell in ws['J']:
            cell.number_format = '0.00%'
        for cell in ws['N']:
            cell.number_format = '0.00%'

    print(f'Exported {excel_path} successfully.')
