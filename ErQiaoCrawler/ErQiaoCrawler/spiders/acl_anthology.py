import scrapy
import os
import glob
import json
from pytube import YouTube


class AclAnthologySpider(scrapy.Spider):
    name = 'acl_anthology'
    allowed_domains = ['www.aclweb.org']
    start_urls = ['https://www.aclweb.org/anthology/']
    base_url = 'www.aclweb.org'
    download_base_path = '/acl/'

    def parse(self, response):
        # 通过xptah爬取url
        # data = response.body
        # soup = BeautifulSoup(data)
        # self.log(soup.prettify())
        # self.log(data)
        # self.log(soup.find_all(id='2020-aacl-main'))
        # self.log(response.xpath('//*[@id="2020-aacl-main"]/p[1]/span[2]/strong/a/text()').extract())
        # self.log(response.xpath('//*[@id="2020-aacl-srw"]/p[1]/span[2]/strong/a/text()').extract())
        # selectors = response.xpath('//*[@id="2020-aacl-main"]/p')
        # selectors = response.xpath('//*[@id="main-container"]/div/div[2]/main/table[1]/tbody/tr')
        # self.logger.debug(len(selectors))
        # selectors = response.xpath('//*[@id="main-container"]/div/div[2]/main/table[1]/tbody/tr[1]/td[.//a]')
        # self.logger.debug(len(selectors))
        # for selector in selectors:
        #     url=selector.xpath('./a/@href')[0].extract()
        #     self.logger.debug(url)
        # 从网页的表格中找url
        # table1
        # acl_selectors = response.xpath('//*[@id="main-container"]/div/div[2]/main/table[1]/tbody/tr')
        # for acl_selector in acl_selectors:
        #     year_selectors = acl_selector.xpath('./td[.//a]')
        #     for year_selector in year_selectors:
        #         url=self.base_url+year_selector.xpath('./a/@href')[0].extract()
        #         self.logger.debug(url)
        #         yield scrapy.Request(url, callback=self.parse_item, dont_filter=False)

        # 网址提供了bib 这里使用bib中的url爬取
        url_list = []  # 62299
        with open('./ErQiaoCrawler/url_list.txt', 'r') as f:
            url_list.extend(f.readlines())
        for i in range(6000, 10000):
            yield scrapy.Request(url_list[i], callback=self.parse_item, dont_filter=False)
        # https://www.aclweb.org/anthology/D18-1353

    def parse_item(self, response):
        # 文章标题
        title = response.xpath('//*[@id="title"]/a//text()').extract()
        # 文章作者
        author_selectors = response.xpath('//*[@id="main"]/p/a')
        authors = []
        for author_selector in author_selectors:
            author = author_selector.xpath('./text()')[0].extract()
            authors.append(author)
        # 文章摘要
        abstract = response.xpath('//*[@id="main"]/div/div[1]/div/div/text()').extract()
        item = {}
        item['title'] = ''.join(title)
        item['authors'] = authors
        item['abstract'] = ''.join(abstract)
        # 其他信息
        key_selectors = response.xpath('//*[@id="main"]/div/div[1]/dl/dt')
        value_selectors = response.xpath('//*[@id="main"]/div/div[1]/dl/dd')
        if len(key_selectors) != len(value_selectors):
            self.logger.debug("出错：acl 爬取字段出错！")
        for i in range(0, len(key_selectors)):
            key = key_selectors[i].xpath('./text()')[0].extract()
            if key.endswith(':'):
                key = key[0:-1]
            # Anthology ID , Month , Year , Address , Publisher , Pages
            tmp1 = value_selectors[i].xpath('./text()')
            # Volume Venue (Video Dataset Software Source )
            tmp2 = value_selectors[i].xpath('./a/text()')
            # Video Dataset Software Source   (多个，需要额外处理)
            tmp3 = value_selectors[i].xpath('./a/@href')
            if len(tmp1) == 1:
                item[key] = tmp1[0].extract()
            if len(tmp2) == 1:
                if key == 'Video' or key == 'Dataset' or key == 'Software' or key == 'Source':
                    if key not in item:
                        item[key] = []
                    item[key].append(tmp2[0].extract().split()[0])  # 去掉xa0字符
                else:
                    item[key] = tmp2[0].extract()
            if len(tmp3) == 1:
                if key == 'Video' or key == 'Dataset' or key == 'Software' or key == 'Source':
                    if key + '_url' not in item:
                        item[key + '_url'] = []
                    item[key + '_url'].append(tmp3[0].extract())
                else:
                    item[key + '_url'] = tmp3[0].extract()

        if 'PDF_url' in item:
            path = self.download_base_path + item['Anthology ID']
            file_name = item['Anthology ID'] + '.pdf'
            if len(glob.glob(pathname=path + "/" + file_name)) > 0:
                pass
            yield scrapy.Request(item['PDF_url'], callback=self.parse_down,
                                 meta={'Anthology ID': item['Anthology ID'],
                                 'file_name': file_name, 'type': 'PDF'}, dont_filter=True)

        file_types = ['Source', 'Dataset', 'Software']
        for file_type in file_types:
            if file_type in item:
                for i in range(0, len(item[file_type])):
                    path = self.download_base_path + item['Anthology ID']
                    file_name = item[file_type][i]
                    if len(glob.glob(pathname=path + "/" + file_name)) > 0:
                        pass
                    yield scrapy.Request(item[file_type + '_url'][i], callback=self.parse_down,
                                         meta={'Anthology ID': item['Anthology ID'],
                                         'file_name': file_name, 'type': file_type}, dont_filter=True)

        if 'Video_url' in item:
            for url in item['Video_url']:
                if 'slideslive' in url:  # 有ppt可爬取
                    ppt_id = url.split('/')[-1]
                    ppt_url = 'https://d2ygwrecguqg66.cloudfront.net/data/presentations/' + ppt_id + '/' + ppt_id + '.xml'
                    yield scrapy.Request(ppt_url, callback=self.parse_ppt_xml, meta={'Anthology ID': item['Anthology ID'],
                                         'ppt_id': ppt_id, 'type': 'slide'}, dont_filter=True)
                    video_id = url.split('/')[-1]
                    video_url = 'https://ben.slideslive.com/player/' + video_id + '?demo=false'
                    yield scrapy.Request(video_url, callback=self.parse_video, meta={'Anthology ID': item['Anthology ID'],
                                         'file_name': video_id + '.mp4', 'type': 'Video'}, dont_filter=True)
                elif 'youtube' in url:  # crossmind中已实现
                    try:
                        video_item = {}
                        video_item['Anthology ID'] = item['Anthology ID']
                        video_item['mark_acl_path'] = 1
                        video_path = YouTube(url).streams.first().download(
                            self.download_base_path + item['Anthology ID'] + "/")
                        video_item['Video_path'] = video_path
                        yield video_item
                    except Exception:
                        self.logger.debug('youbute视频下载失败' + str(item['Anthology ID']))
                        with open(self.download_base_path + 'error.txt', 'a+') as f:
                            f.write(url + '\n')

                elif 'vimeo' in url:  # crossmind中已实现
                    vimeo_id = url.split('/')[-1]
                    vimeo_url = 'https://player.vimeo.com/video/' + vimeo_id + '/config?autopause=1&byline=0\
                                 &collections=1&context=Vimeo%5CController%5CClipController.main&default_to_hd=1\
                                 &outro=nothing&portrait=0&share=1&title=0&watch_trailer=0'
                    yield scrapy.Request(vimeo_url, callback=self.parse_vimeo, meta={'Anthology ID': item['Anthology ID'],
                                         'file_name': vimeo_id + '.mp4', 'type': 'Video'}, dont_filter=True)
                    pass
        yield item  # Anthology ID
        pass

    # pdf zip slide video
    def parse_down(self, response):
        path = self.download_base_path + response.meta['Anthology ID']
        file_name = response.meta['file_name']
        file_tyle = response.meta['type']
        if file_tyle == 'slide':
            path = response.meta['path']
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            with open(path + "/" + file_name, 'wb') as file:
                file.write(response.body)
            item = {}
            item['Anthology ID'] = response.meta['Anthology ID']
            item[file_tyle + '_path'] = path + "/" + file_name
            item['mark_acl_path'] = 1
            yield item
        except Exception:
            self.logger.debug('文件下载失败' + response.meta['Anthology ID'])
            with open(self.download_base_path + 'error.txt', 'a+') as f:
                f.write(response.url + '\n')

    # 幻灯片
    def parse_ppt_xml(self, response):
        from xml.dom.minidom import parseString
        domTree = parseString(response.text)
        rootNode = domTree.documentElement
        slides = rootNode.getElementsByTagName("slide")
        for slide in slides:
            ppt_id = response.meta['ppt_id']
            path = self.download_base_path + response.meta['Anthology ID'] + '/' + ppt_id
            file_name = slide.childNodes[3].childNodes[0].data + '.jpg'
            if len(glob.glob(pathname=path + "/" + file_name)) > 0:
                pass
            url = 'https://d2ygwrecguqg66.cloudfront.net/data/presentations/' + ppt_id + '/slides/medium/' + file_name
            yield scrapy.Request(url, callback=self.parse_down, meta={'Anthology ID': response.meta['Anthology ID'],
                                 'file_name': file_name, 'type': 'slide', 'path': path}, dont_filter=True)

    # vimeo
    def parse_video(self, response):
        vimeo_id = json.loads(response.text)['video_service_id']
        vimeo_url = 'https://player.vimeo.com/video/' + vimeo_id + '/config?autopause=1&byline=0\
                &collections=1&context=Vimeo%5CController%5CClipController.main&default_to_hd=1\
                &outro=nothing&portrait=0&share=1&title=0&watch_trailer=0'
        yield scrapy.Request(vimeo_url, callback=self.parse_vimeo, meta={'Anthology ID': response.meta['Anthology ID'],
                             'file_name': response.meta['file_name'], 'type': response.meta['type']}, dont_filter=True)

    def parse_vimeo(self, response):
        res_dict = json.loads(response.text)['request']['files']['progressive']
        # 选清晰度最低的 流量有限
        height = 1080
        video_url = ''
        for res in res_dict:
            if height > res['height']:
                height = res['height']
                video_url = res['url']

        path = self.download_base_path + response.meta['Anthology ID']
        file_name = response.meta['file_name']
        if len(glob.glob(pathname=path + "/" + file_name)) > 0:
            pass
        yield scrapy.Request(video_url, callback=self.parse_down, meta={'Anthology ID': response.meta['Anthology ID'],
                             'file_name': response.meta['file_name'], 'type': response.meta['type']}, dont_filter=True)
