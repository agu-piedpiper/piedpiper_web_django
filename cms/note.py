import requests
import json
import pandas as pd
import re,urllib,os

class Note:
    def get_deta(self):
        api_url = "https://note.com/api/v2/creators/piedpiper_aoyama/contents?kind=note"
        notes_url = "https://note.com/api/v1/notes/"
        urlname = "piedpiper_aoyama"

        # 総記事件数の取得
        # payload = {'urlname': urlname}
        res = requests.get("https://note.com/api/v2/creators/"+urlname).content

        df = json.loads(res)
        note_count = df['data']['noteCount']

        # 総取得ページ数
        df = []
        page_num = (note_count//6) + 1
        for page in range(page_num):
            payload = {'page': page+1}
            res = requests.get(api_url, params=payload).content
            a = json.loads(res)["data"]["contents"]
            df.extend(a)
        return df

    def get_note(self, id):
        notes_url = "https://note.com/api/v1/notes/"
        res = requests.get(notes_url + str(id)).content
        df = json.loads(res)
        note = df["data"]

        return note


class Image():
    
    def download_img(url,dst_path):
        try:
            with urllib.request.urlopen(url) as web_file, open(dst_path, 'wb') as local_file:
                local_file.write(web_file.read())
        except urllib.error.URLError as e:
            print(e)

    def get_img_position(note_body):
        first_find_words = 'https://d2l930y2yx77uc.cloudfront.net/production/uploads/images/'
        end_find_words = '(.png|.jpg|.jpeg)'
        find_words=f'{first_find_words}.*?{end_find_words}'
        img_positon = [m.span() for m in re.finditer(find_words, note_body)]
        # [(2, 4), (6, 8)]

        return img_positon

    def rewriting_img_path(note_body,id):
        note_img_positions = Image.get_img_position(note_body)
        word_len_diff=0
        for index,note_img_position in enumerate(note_img_positions):
            first,end = note_img_position
            img_url=note_body[first-word_len_diff:end-word_len_diff]
            # img_extension=img_url[-4:]
            img_extension=re.findall('[a-z]+$', img_url)[0]
            if img_extension == 'jpeg':
                img_extension = 'jpg'
            image_name = f'{id}_{index}'
        
            dst_path=f'./media/images/{image_name}.{img_extension}'
            
            Image.download_img(img_url,dst_path)
            note_body = note_body.replace(img_url,dst_path[1:])
            word_len_diff += len(img_url)-len(dst_path[1:])
    
        return note_body

    def rename_eyecatch(dl_img_path,activity_id):
        
        dl_img_path=dl_img_path.split("?")[0]
        extension = os.path.splitext(dl_img_path)[1]
        image_name='eyecatch'

        if extension ==".jpeg":
            extension = ".jpg"
        dst_path=f'./media/images/eyecatch_activity_{activity_id}{extension}'
        Image.download_img(dl_img_path,dst_path)
        eyecatch_img_path = dst_path[8:]

        return eyecatch_img_path