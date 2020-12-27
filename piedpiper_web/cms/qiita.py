import requests
import json
import pandas as pd
import re, urllib, os
from PIL import Image, ImageFont, ImageDraw

class Qiita():
    def get_deta(self):
        # 総記事の取得
        users = ['petaexazettayotta', 'MLL', 'dddddddddd']  # 記事を取得するユーザリスト。(適当なユーザ)
        api_url = 'https://qiita.com/api/v2/'
        df = []
        for user in users:
            res = requests.get(f'{api_url}users/{user}/items').content
            a = json.loads(res)
            df.extend(a)
        # 総記事数
        qiita_count = len(df)

        return df

    def get_qiita(self, id):    #特定記事の取得(idで指定)
        qiita_url = 'https://qiita.com/api/v2/'
        res = requests.get(f'{qiita_url}items/{id}').content
        qiita = json.loads(res)

        return qiita


class Image():
    def make_eyecatch(contents, dst_path, font_size=54, height=658, width=1250, font_color=(51, 51, 51), max_title_length=810, max_user_length=740):
        img_path = 'techblog_thumbnail_background.png'
        img = Image.open(img_path).copy()
        title = contents[0]
        title2 = None
        user = '@' + contents[1]
        font = ImageFont.truetype(font='/content/ヒラギノ角ゴシック W6.ttc', size=font_size)
        draw = ImageDraw.Draw(img)
        if draw.textsize(title, font=font)[0] > max_title_length:
            title2 = title[20:40]
            title = title[:20]
        if draw.textsize(user, font=font)[0] > max_user_length:
            while draw.textsize(user, font=font)[0] > max_user_length:
                user = user[:-1]

        title_w, title_h = draw.textsize(title, font=font)
        if title2 is not None:
            title2_w, title2_h = draw.textsize(title2, font=font)
            draw.text(((width -title2_w)/2, 290 + title_h), title2, font_color, font=font)
        draw.text(((width -title_w)/2, 260), title, font_color, font=font)

        user_w, user_h = draw.textsize(user, font=font)
        draw.text(((width -user_w -200), 520), user, font_color, font=font)

        img.save(dst_path, "PNG")

    def download_img(url,dst_path):
        try:
            with urllib.request.urlopen(url) as web_file, open(dst_path, 'wb') as local_file:
                local_file.write(web_file.read())
        except urllib.error.URLError as e:
            print(e)

    def get_img_position(qiita_body):
        first_find_words = 'https://qiita-user-contents.imgix.net/'
        end_find_words = '(.png|.jpg|.jpeg)'
        find_words = f'{first_find_words}.*?{end_find_words}'
        img_positon = [m.span() for m in re.finditer(find_words, note_body)]
        # [(2, 4), (6, 8)]

        return img_positon

    def rewriting_img_path(qiita_body,id):
        qiita_img_positions = Image.get_img_position(qiita_body)
        word_len_diff = 0
        for index, qiita_img_position in enumerate(qiita_img_positions):
            first, end = qiita_img_position
            img_url = qiita_body[first-word_len_diff:end-word_len_diff]
            # img_extension=img_url[-4:]
            img_extension = re.findall('[a-z]+$', img_url)[0]
            if img_extension == 'jpeg':
                img_extension = 'jpg'
            image_name = f'{id}_{index}'

            dst_path = f'./media/images/{image_name}.{img_extension}'

            Image.download_img(img_url, dst_path)
            qiita_body = qiita_body.replace(img_url, dst_path[1:])
            word_len_diff += len(img_url) - len(dst_path[1:])

        return qiita_body

    def rename_eyecatch(eyecatch_property, qiita_id):
        dst_path = f'./media/images/eyecatch_qiita_{qiita_id}.jpg'
        eyecatch_img = Image.make_eyecatch(eyecatch_property, dst_path)
        eyecatch_img_path = dst_path[8:]

        return eyecatch_img_path
