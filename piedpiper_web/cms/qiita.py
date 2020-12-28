import requests
import json
import pandas as pd
import re, urllib, os
import requests  # Webページ取得
import lxml.html  # スクレイピング

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

    def download_img(url,dst_path):
        try:
            with urllib.request.urlopen(url) as web_file, open(dst_path, 'wb') as local_file:
                local_file.write(web_file.read())
        except urllib.error.URLError as e:
            print(e)

    def get_eyecatch(url, dst_path):
        res = requests.get(url)
        html = lxml.html.fromstring(res.content)    # スクレイピング
        img_url = html.xpath('.//meta[@property="og:image"]/@content')  # OGP画像のURLを取得

        return img_url[0]

    def get_img_position(qiita_body):
        first_find_words = 'https://qiita-image-store.'
        end_find_words = '(.png|.jpg|.jpeg)'
        find_words = f'{first_find_words}.*?{end_find_words}'
        img_positon = [m.span() for m in re.finditer(find_words, qiita_body)]
        # [(2, 4), (6, 8)]

        return img_positon

    def rewriting_img_path(qiita_body, id):
        qiita_img_positions = Image.get_img_position(qiita_body)
        word_len_diff = 0
        img_urls = []
        for index, qiita_img_position in enumerate(qiita_img_positions):
            first, end = qiita_img_position
            img_url = qiita_body[first-word_len_diff:end-word_len_diff]
            img_urls.append(img_url)
            img_extension = re.findall('[a-z]+$', img_url)[0]
            if img_extension == 'jpeg':
                img_extension = 'jpg'
            image_name = f'{id}_{index}'

            dst_path = f'./media/images/{image_name}.{img_extension}'

            Image.download_img(img_url, dst_path)
            qiita_body = qiita_body.replace(img_url, dst_path[1:])
            word_len_diff += len(img_url) - len(dst_path[1:])

        return qiita_body

    def rename_eyecatch(qiita_url, qiita_id):
        dst_path = f'./media/images/eyecatch_qiita_{qiita_id}.jpg'
        dl_img_path = Image.get_eyecatch(qiita_url, dst_path)
        Image.download_img(dl_img_path, dst_path)
        eyecatch_img_path = dst_path[8:]

        return eyecatch_img_path
