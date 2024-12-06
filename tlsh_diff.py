import sqlite3
from concurrent.futures import ThreadPoolExecutor, as_completed

import tlsh
from tqdm import tqdm


def calculate_diff(pair):
    sha256_1 = pair[0]
    tlsh_1 = pair[1]
    sha256_2 = pair[2]
    tlsh_2 = pair[3]
    diff = tlsh.diff(tlsh_1, tlsh_2)
    return sha256_1, sha256_2, diff


with sqlite3.connect(r'C:\Users\ikaro\.maldb\db\malware.db') as conn:
    c = conn.cursor()
    c.execute('''
    select a.sha256 as sha256_1, a.tlsh as tlsh_1, b.sha256 as sha256_2, b.tlsh as tlsh_2
      from malware_info a
               join malware_info b
                    on a.rowid < b.rowid
    ''')
    rows = c.fetchall()
    # c.execute('select sha256, tlsh from malware_info')
    # rows = c.fetchall()
    c.close()

# pairs = [
#     (rows[i], rows[j])
#     for i in range(len(rows))
#     for j in range(i + 1, len(rows))
# ]

lst = []
with ThreadPoolExecutor() as executor:
    tasks = [
        executor.submit(calculate_diff, row)
        for row in rows
    ]

    for task in tqdm(as_completed(tasks), total=len(rows)):
        lst.append(task.result())

with sqlite3.connect(r'C:\Users\ikaro\.maldb\db\malware.db') as conn:
    cursor = conn.cursor()
    cursor.executemany('insert or ignore into tlsh_similarity values (?, ?, ?)', lst)
    rows = cursor.fetchall()
    conn.close()
