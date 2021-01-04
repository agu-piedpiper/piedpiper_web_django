import json
import urllib
import lxml.html
import requests
from accounts.models import CustomUser
from cms.models import Techblog, Techcategory


class Qiita():
    def get_qiita_user_ids(self):
        """
        全CustomUserのQiitaユーザidの取得
        @return: Qiitaユーザidのリスト
        @rtype: list
        """
        return CustomUser.objects.all().distinct('qiita_user_id').values_list('qiita_user_id', flat=True)

    def get_posts(self, qiita_user_ids):
        """
        Qiitaユーザの記事一覧取得
        @param qiita_user_ids: Qiitaユーザidのリスト
        @type qiita_user_ids: list
        @return: Qiitaの記事一覧データ
        @rtype: list
        """
        # 総記事の取得
        api_url = 'https://qiita.com/api/v2/users/'
        result = []
        for id in qiita_user_ids:
            res = requests.get(f'{api_url}{id}/items').content
            result.extend(json.loads(res))

        return result

    def get_post(self, id):
        """
        idの記事の取得
        @param id: Qiita記事のid
        @type id: str
        @return: Qiita記事のデータ
        @rtype: dict
        """
        api_url = 'https://qiita.com/api/v2/items/'
        res = requests.get(f'{api_url}{id}').content

        return json.loads(res)
    
    def import_qiita(self, qiita_posts):
        """
        未登録のQiita記事をDBに登録する
        @param qiita_posts: Qiitaの記事一覧データ
        @type qiita_posts: list
        """
        # 登録済qiita記事idを取得
        registered_qiita_item_id = Techblog.objects.exclude(
            qiita_item_id=None).values_list('qiita_item_id', flat=True)
        # qiita記事をDBに登録
        for n in qiita_posts:
            qiita_item_id = n['id']
            if qiita_item_id not in registered_qiita_item_id:
                post_data = self.get_post(qiita_item_id)
                techblog = Techblog()
                techblog.title = n['title']
                techblog.body = self.__convert_body(post_data)
                techblog.qiita_item_id = qiita_item_id
                techblog.custom_user__qiita_user_id = n['user']['id']
                techblog.image = self.__set_thumbnail(post_data)
                techblog.is_qiita = True
                techblog.save()
                self.__set_categories(techblog, post_data)

    def __set_categories(self, post, post_data):
        """
        Qiita記事のカテゴリ名の登録
        @param post: techblogインスタンス
        @type post: <class 'cms.models.Techblog'>
        @param post_data: Qiita記事データ
        @type post_data: dict
        """
        registered_techcategory = Techcategory.objects.exclude(name=None).values_list('name', flat=True)
        tags = [i['name'] for i in post_data['tags']]
        for tag in tags:
            if tag not in registered_techcategory:
                tag = Techcategory.objects.create(name=tag)
            else:
                tag = Techcategory.objects.get(name=tag)
            post.categories.add(tag)
        post.save()

    def __set_thumbnail(self, post_data):
        """
        Qiita記事のサムネイル画像pathの取得
        @param post_data: Qiita記事データ
        @type post_data: dict
        @return: 画像のパス
        @rtype: str
        """
        dst_path = f'./media/images/thumbnail_qiita_{post_data["id"]}.png'
        dl_img_path = self.__get_thumbnail_url(post_data['url'])
        self.__download_img(dl_img_path, dst_path)

        return dst_path[8:]

    def __get_thumbnail_url(self, url):
        """
        Qiita記事のサムネイル画像URLの取得
        @param url: Qiita記事のURL
        @type url: str
        @return: サムネイル画像のURL
        @rtype: str
        """
        res = requests.get(url)
        html = lxml.html.fromstring(res.content)    # スクレイピング
        img_url = html.xpath('.//meta[@property="og:image"]/@content')  # OGP画像のURLを取得

        return img_url[0]
    
    def __convert_body(self, post_data):
        """
        Qiita記事のHTMLをTechblog用に変換
        @param post_data: Qiita記事データ
        @type post_data: dict
        @return: 画像パス変換済のQiita記事データ
        @rtype: dict
        """
        rendered_body = post_data["rendered_body"]
        html = lxml.html.fromstring(rendered_body)
        targets = html.cssselect('img')
        for index, target in enumerate(targets):
            # 画像パスを取得
            src = target.get("src").replace('&', '&amp;')
            srcset = target.get("srcset")
            data_canonical_src = target.get("data-canonical-src")
            img_url = src.split('?')[0]
            img_extension = img_url.split('.')[-1]
            if img_extension == 'jpeg':
                img_extension = 'jpg'
            # 画像保存先パス
            dst_path = f"./media/images/{post_data['id']}_{index}.{img_extension}"
            # 画像ダウンロード
            self.__download_img(src, dst_path)
            # HTMLの画像パスを書き換え
            path = dst_path[1:]
            rendered_body = rendered_body.replace(src, path)
            if srcset is not None:
                rendered_body = rendered_body.replace(srcset.replace('&', '&amp;'), path + ' 1x')
            if data_canonical_src is not None:
                rendered_body = rendered_body.replace(data_canonical_src.replace('&', '&amp;'), path)
        # HTMLを返却
        return rendered_body

    def __download_img(self, url, dst_path):
        """
        画像を保存
        @param url: ソース画像URL
        @type url: str
        @param dst_path: 保存先パス
        @type dst_path: str
        """
        try:
            with urllib.request.urlopen(url) as web_file, open(dst_path, 'wb') as local_file:
                local_file.write(web_file.read())
        except urllib.error.URLError as e:
            print(e)



