
import requests
import json
import pandas as pd
import re,urllib

class Image():
    
    def download_img(url,dst_path):
        try:
            with urllib.request.urlopen(url) as web_file, open(dst_path, 'wb') as local_file:
                local_file.write(web_file.read())
        except urllib.error.URLError as e:
            print(e)

    def get_img_position(note_body):
        first_find_words = 'https://d2l930y2yx77uc.cloudfront.net/production/uploads/images/'
        end_find_words = '(.png|.jpg)'
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
            img_extension=img_url[-4:]
            image_name = f'{id}_{index}'
            
            dst_path=f'./media/images/{image_name}{img_extension}'
            Image.download_img(img_url,dst_path)
            note_body = note_body.replace(img_url,dst_path)
            word_len_diff += len(img_url)-len(dst_path)
    
        return note_body

# body='''<img src="https://d2l930y2yx77uc.cloudfront.net/production/uploads/images/12665384/picture_pc_ed8308a5ad3efe049456c8bd867f4267.png"aaasrc="https://d2l930y2yx77uc.cloudfront.net/production/uploads/images/14452201/picture_pc_d77aeaa4285b7c3beb0183af5995faee.jpg"'''
# body=body.replace('\n' , '' )
# note_body=Image.rewriting_img_path(body,2)
# print(note_body)