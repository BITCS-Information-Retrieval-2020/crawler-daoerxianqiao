import scrapy
from pytube import YouTube
import json
import threading
import os
import glob


class CrossmindSpider(scrapy.Spider):
    name = 'crossmind'
    allowed_domains = ['crossminds.ai']
    start_urls = ['https://crossminds.ai']
    base_url = 'https://api.crossminds.io/web/node/video/name/'
    comment_base_url = 'https://activity.crossminds.io/comment/target'
    reaction_base_url = 'https://api.crossminds.io/web/reactive/comment/'
    # crossmind网站中视频分类（按照领域）
    node_name = ['knowledge-engineering', 'ai-safety', 'information-retrieval',
                 'machine-learning-fairness', 'audio-processing', 'data-science',
                 'causal-inference', 'basic-theory', 'autonomous-driving',
                 'sequential', 'recommender-system', 'natural-language-processing',
                 'adversarial-training', 'robotics', 'generative-models',
                 'optimization', 'graphs', 'deep-learning', 'machine-learning',
                 'neural-network', 'computer-vision']

    node_index = 0
    limit = 24
    offset = 0
    video_base_path = '/crossmind/video/'
    pdf_base_path = '/crossmind/pdf/'
    comment_limit = 3
    # 只更新评论和reaction
    update_c_r_only = False

    def parse(self, response):
        url = self.base_url + self.node_name[self.node_index] + '?limit=' + str(self.limit) + '&offset=' + str(self.offset)
        yield scrapy.Request(url, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        res_dict = json.loads(response.text)
        next_request = res_dict['next_request']
        results = res_dict['results']
        for re in results:
            if not self.update_c_r_only:
                yield re
            target_id = re['foreign_id']
            # 1.YouTube download 2.CrossMinds
            source = re['source']
            video_url = re['video_url']
            attachments = re['attachment']

            # 爬取pdf
            for attachment in attachments:
                if attachment['name'] == 'Paper Link':
                    # arxiv 链接可能直接是pdf 也可能需要进一步修改链接
                    pdf_url = ''
                    if attachment['source_link'].endswith('.pdf'):
                        pdf_url = pdf_url + attachment['source_link']
                    elif 'arxiv' in attachment['source_link']:
                        arxiv_id = attachment['source_link'].split('/')[4]
                        arxiv_id = arxiv_id.split('#')[0]
                        pdf_url = pdf_url = pdf_url + 'https://arxiv.org/pdf/' + arxiv_id + '.pdf'
                    elif 'openaccess' in attachment['source_link']:
                        pdf_url = pdf_url + attachment['source_link']
                    elif 'drive' in attachment['source_link'] and 'google' in attachment['source_link']:
                        drive_id = attachment['source_link'].split('/')[-2]
                        pdf_url = pdf_url + 'https://drive.google.com/uc?id=' + drive_id + '&export=download'
                    elif 'aclweb' in attachment['source_link']:
                        if attachment['source_link'].endswith('/'):
                            pdf_url = pdf_url + attachment['source_link'][0:-1] + '.pdf'
                        else:
                            pdf_url = pdf_url + attachment['source_link'] + '.pdf'
                    pdf_num = len(glob.glob(pathname=self.pdf_base_path + target_id + "/*.pdf"))
                    if pdf_num == 0:
                        if pdf_url != '':
                            yield scrapy.Request(pdf_url, callback=self.parse_pdf_down,
                                                 meta={'target_id': target_id}, dont_filter=True)
                        else:
                            with open(self.pdf_base_path + 'miss.txt', 'a+') as f:
                                f.write(attachment['source_link'] + '\n')
                    break

            # 爬取视频
            if not self.update_c_r_only:
                video_num = len(glob.glob(pathname=self.video_base_path + target_id + "/*.mp4"))
                if video_num == 0 and (source == 'YouTube download' or source == 'YouTube'):
                    self.logger.debug('youbute视频ing')
                    yield scrapy.Request(video_url, callback=self.parse_youtube,
                                         meta={'target_id': target_id, 'remianing': 2}, dont_filter=True)
                elif video_num == 0 and source == 'CrossMinds':
                    self.logger.debug('m3u8视频ing')
                    yield scrapy.Request(video_url, callback=self.parse_m3u8,
                                         meta={'target_id': target_id}, dont_filter=True)
                elif video_num == 0 and source == 'Vimeo':
                    self.logger.debug('vimeo视频ing')
                    vimeo_id = video_url.split('/')[-1]
                    vimeo_url = 'https://player.vimeo.com/video/' + vimeo_id + '/config?autopause=1&byline=0\
                            &collections=1&context=Vimeo%5CController%5CClipController.main&default_to_hd=1\
                            &outro=nothing&portrait=0&share=1&title=0&watch_trailer=0'
                    yield scrapy.Request(vimeo_url, callback=self.parse_vimeo,
                                         meta={'target_id': target_id}, dont_filter=True)

            # 爬取评论
            url = self.comment_base_url + '?target_id=' + target_id + \
                '&target_type=video&parent_id=&root_id=&reply_limit=3&order=-1&sort=like_count' + \
                '&offset=0' + '&limit=' + str(self.comment_limit)
            yield scrapy.Request(url, callback=self.parse_comment,
                                 meta={'offset': 0, 'target_id': target_id}, dont_filter=True)

            # 爬取reaction
            url = self.reaction_base_url + target_id
            yield scrapy.Request(url, callback=self.parse_reaction, dont_filter=True)

        if 'limit' in next_request:
            url = self.base_url + self.node_name[self.node_index] + '?limit=' + str(self.limit) + \
                '&offset=' + str(next_request['offset'])
            yield scrapy.Request(url, callback=self.parse_item, dont_filter=True)
        elif self.node_index < len(self.node_name) - 1:
            self.logger.debug(self.node_name[self.node_index] + ':爬取结束')
            self.node_index = self.node_index + 1
            url = self.base_url + self.node_name[self.node_index] + '?limit=' + str(self.limit) + '&offset=' + str(self.offset)
            yield scrapy.Request(url, callback=self.parse_item, dont_filter=True)
        else:
            self.logger.debug('全部爬取结束')

    def parse_pdf_down(self, response):
        path = self.pdf_base_path + response.meta['target_id']
        file_name = response.meta['target_id'] + '.pdf'
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            with open(path + "/" + file_name, 'wb') as file:
                file.write(response.body)
            item = {}
            item['target_id'] = response.meta['target_id']
            item['pdf_path'] = path + "/" + file_name
            yield item
        except Exception:
            self.logger.debug('文件下载失败' + response.meta['Anthology ID'])
            with open(self.pdf_base_path + 'error.txt', 'a+') as f:
                f.write(response.url + '\n')

    def parse_youtube(self, response):
        try:
            video_item = {}
            video_item['target_id'] = response.meta['target_id']
            video_path = YouTube(response.url).streams.first().download(
                self.video_base_path + response.meta['target_id'] + "/")
            video_item['video_path'] = video_path
            yield video_item
        except Exception:
            self.logger.debug('youbute视频下载失败' + str(video_item['target_id']))
            if response.meta['remianing'] > 0:  # 429 但作用好像不大
                yield scrapy.Request(response.url, callback=self.parse_youtube,
                                     meta={'target_id': response.meta['target_id'],
                                           'remianing': response.meta['remianing'] - 1}, dont_filter=True)
            else:
                with open(self.video_base_path + 'error.txt', 'a+') as f:
                    f.write(response.url + '\n')

    def parse_m3u8(self, response):
        ts_base_url = response.url.replace(response.url.split('/')[-1], '')
        # 下载ts文件
        ts_list = []
        for ts in response.text.splitlines():
            if ts.endswith('.ts'):
                ts_list.append(ts)
        for ts in ts_list:
            yield scrapy.Request(ts_base_url + ts, callback=self.parse_m3u8_down, meta={
                                 'target_id': response.meta['target_id'], 'ts': ts,
                                 'ts_list': ts_list}, dont_filter=True)

    def parse_m3u8_down(self, response):
        if not os.path.exists(self.video_base_path + response.meta['target_id']):
            os.makedirs(self.video_base_path + response.meta['target_id'])
        try:
            with open(self.video_base_path + response.meta['target_id'] + "/" + response.meta['ts'], 'wb') as file:
                file.write(response.body)
            # 整合ts文件
            ts_num = len(glob.glob(pathname=self.video_base_path + response.meta['target_id'] + "/*"))
            if ts_num == len(response.meta['ts_list']):
                video_path = self.video_base_path + response.meta['target_id'] + "/" + response.meta['target_id'] + ".mp4"
                try:
                    with open(video_path, 'wb+') as f:
                        for i in range(len(response.meta['ts_list'])):
                            tmp_path = self.video_base_path + response.meta['target_id'] + "/" + response.meta['ts_list'][i]
                            f.write(open(tmp_path, 'rb').read())
                    video_item = {}
                    video_item['target_id'] = response.meta['target_id']
                    video_item['video_path'] = video_path
                    yield video_item
                except Exception:
                    self.logger.debug('ts文件整合失败' + str(response.meta['target_id']))
        except Exception:
            self.logger.debug('ts文件下载失败' + str(response.meta['target_id']))
            with open(self.video_base_path + 'error.txt', 'a+') as f:
                f.write(response.url + '\n')

    def parse_vimeo(self, response):
        res_dict = json.loads(response.text)['request']['files']['progressive']
        # 选清晰度最低的 流量不够
        height = 1080
        video_url = ''
        for res in res_dict:
            if height > res['height']:
                height = res['height']
                video_url = res['url']
        yield scrapy.Request(video_url, callback=self.parse_vimeo_download,
                             meta={'target_id': response.meta['target_id']}, dont_filter=True)

    def parse_vimeo_download(self, response):
        if not os.path.exists(self.video_base_path + response.meta['target_id']):
            os.makedirs(self.video_base_path + response.meta['target_id'])
        try:
            video_path = self.video_base_path + response.meta['target_id'] + "/" + response.meta['target_id'] + ".mp4"
            with open(video_path, 'wb') as file:
                file.write(response.body)
            video_item = {}
            video_item['target_id'] = response.meta['target_id']
            video_item['video_path'] = video_path
            yield video_item
        except Exception:
            self.logger.debug('vimeo文件下载失败' + str(response.meta['target_id']))
            with open(self.video_base_path + 'error.txt', 'a+') as f:
                f.write(response.url + '\n')

    def parse_comment(self, response):
        res_dict = json.loads(response.text)
        comments = res_dict['data']
        if len(comments) > 0:
            for comment in comments:
                yield comment
        if 'has_next' in res_dict and res_dict['has_next']:
            offset = response.meta['offset'] + self.comment_limit
            url = self.comment_base_url + '?target_id=' + response.meta['target_id'] + \
                '&target_type=video&parent_id=&root_id=&reply_limit=3&order=-1&sort=like_count' + \
                '&offset=' + str(offset) + '&limit=' + str(self.comment_limit)
            yield scrapy.Request(url, callback=self.parse_comment,
                                 meta={'offset': offset, 'target_id': response.meta['target_id']}, dont_filter=True)

    def parse_reaction(self, response):
        res_dict = json.loads(response.text)
        results = res_dict['results']
        for r in results:
            yield r
