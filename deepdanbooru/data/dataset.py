import os
import sqlite3


def load_tags(tags_path):
    with open(tags_path, 'r') as tags_stream:
        tags = [tag for tag in (tag.strip() for tag in tags_stream) if tag]
        return tags


def load_image_records(sqlite_path, minimum_tag_count):
    if not os.path.exists(sqlite_path):
        raise Exception(f'SQLite database is not exists : {sqlite_path}')

    connection = sqlite3.connect(sqlite_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    image_folder_path = os.path.join(os.path.dirname(sqlite_path), '../scaled/')

    cursor.execute(
        "SELECT id, md5, file_ext, tag_string FROM posts WHERE (file_ext = 'png' OR file_ext = 'jpg' OR file_ext = 'jpeg') ORDER BY id")

    rows = cursor.fetchall()

    image_records = []

    for row in rows:
        ID = row['id']
        md5 = row['md5']
        extension = row['file_ext']
        file_name='e621_'+str(ID)+'_'+md5+'.'+extension
        image_path = os.path.join(
            image_folder_path ,  md5[0:2],file_name)
        tag_string = row['tag_string']

        image_records.append((image_path, tag_string))

    connection.close()

    return image_records
