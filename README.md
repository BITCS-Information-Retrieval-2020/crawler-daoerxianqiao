# crawler-daoerxianqiao

![avatar](https://github.com/BITCS-Information-Retrieval-2020/crawler-daoerxianqiao/blob/main/extra/logo.jpg)


## 项目介绍

总项目为搭建一个学术论文的综合搜索引擎，用户可以检索到一篇论文的综合信息，不仅有pdf文件，还有oral视频，数据集，源代码等多模态信息。

本项目属于总项目中的爬虫模块，提供一个MongoDB数据库和磁盘文件。

<center>


![](https://img.shields.io/badge/flake8-%E9%80%9A%E8%BF%87-green)   ![](https://img.shields.io/badge/%E4%BA%8C%E4%BB%99%E6%A1%A5-%E5%88%B0%E8%BE%BE-red)  ![](https://img.shields.io/badge/%E6%88%90%E5%8D%8E%E5%A4%A7%E9%81%93-%E5%88%B0%E8%BE%BE-red)

</center>


    “你这爬虫能爬吗？”
    “能爬，只能爬亿点点。”
                ————到二仙桥小组

## 目录

- [crawler-daoerxianqiao](#crawler-daoerxianqiao)
  - [项目介绍](#项目介绍)
  - [目录](#目录)
  - [到二仙桥(daoerxianqiao)小组分工](#到二仙桥daoerxianqiao小组分工)
  - [特别致谢](#特别致谢)
  - [爬取数据](#爬取数据)
    - [统计信息（截至到 2021年01月06日）](#统计信息截至到-2021年01月06日)
    - [字段说明](#字段说明)
      - [Corssmind中视频基本信息](#corssmind中视频基本信息)
      - [Corssmind中评论信息](#corssmind中评论信息)
      - [Corssmind中reaction信息](#corssmind中reaction信息)
      - [ACL_Anthology基本信息](#acl_anthology基本信息)
  - [爬虫模块](#爬虫模块)
    - [Crossmind](#crossmind)
      - [视频基本信息](#视频基本信息)
      - [评论信息](#评论信息)
      - [reaction信息](#reaction信息)
      - [PDF文件爬取](#pdf文件爬取)
      - [视频文件爬取](#视频文件爬取)
        - [Youtube](#youtube)
        - [CrossMinds_m3u8](#crossminds_m3u8)
        - [Vimeo](#vimeo)
    - [ACL_Anthology](#acl_anthology)
      - [基本信息](#基本信息)
      - [PDF、Dataset、Source等](#pdfdatasetsource等)
      - [幻灯片](#幻灯片)
      - [Vimeo](#vimeo-1)
  - [特别说明](#特别说明)


## 到二仙桥(daoerxianqiao)小组分工

姓名 | 学号 | 分工 |
:-: | :-: | :-: |
[@姜景虎](https://github.com/Jiangjinghu) | 3120201032 | CrossMinds、ACL Anthology |
[@郑洪超](https://github.com/) | 3220201025 |数据库和CrossMinds:基本信息、视频、PDF |
[@杨俊](https://github.com/) | 3120201087 | 数据库和CrossMinds:基本信息、视频、PDF |
[@寇桓锦](https://github.com/) | 3220200896 | CrossMinds:基本信息、视频、PDF |
[@朱牛牛](https://github.com/) | 3120201113 | ACL Anthology:基本信息、视频、PDF |
[@张鑫](https://github.com/) | 3220201014 |ACL Anthology:基本信息、视频、PDF  |
[@周长智](https://github.com/) | 3120201101 | ACL Anthology:基本信息、视频、PDF |

## 特别致谢
- 感谢**姜景虎**、**王文煊**与**杨俊**的校园网流量
- 感谢**郑洪超**提供的科学上网工具

## 爬取数据

主要爬取了两个网站的数据：

- CrossMinds：[https://crossminds.ai](https://crossminds.ai)（含视频、介绍文字、代码链接等）
  
- ACL Anthology：[https://www.aclweb.org/anthology/](https://www.aclweb.org/anthology/)（含PDF、视频、数据集链接等）

### 统计信息（截至到 2021年01月06日）

网站 | 数据总量 | 本地视频数量 | 本地PDF数量 |  本地PPT份数 | 本地其他附件数量
:-: | :-: | :-: | :-: | :-: | :-: |
CrossMinds| 2686 + 15 + 193 | 2207 | 351 | - | - |  
ACL Anthology| 57791 | 1331 | 57305 | 1117 | 386 |

### 字段说明

字段问题请联系[QQ:3040553715](3040553715@qq.com)，可以处理一下存到其他表中（比如选取一些字段、修改字段名等）。

#### Corssmind中视频基本信息

主要字段 | 类型 | 说明 |
:-: | :-: | :-: |
foreign_id| 字符串 | 视频的唯一标识 |
title| 字符串 | 视频的标题 |
description| 字符串 | 视频的描述 |
thumbnail_url| 字符串 | 视频封面url |
attachment| 字段 | 包括论文链接、代码链接等 |
video_length| 整型 | 视频长度，单位/秒 |
video_url| 字符串 | 视频url |
video_path| 字符串 | 视频在本地磁盘路径 |
pdf_path| 字符串 | pdf在本地磁盘路径 |
view_count| 整型 | 观看数 |
tag| 字符串数组 | 视频标签 |
category| 字符串数组 | 视频内容类型 |

<details>

<summary>table_name: crossmind
</summary>

```json
{
    "_id": ObjectId("5fe1a2b602046584bbe9d69d"),
    "attachment": [ ],
    "author": {
        "id": "5f59132b4ee80ca4db3510da",
        "name": "IGNACIO HUITZIL VELASCO"
    },
    "author_id": "5f59132b4ee80ca4db3510da",
    "category": [
        "ECAI 2020"
    ],
    "collection_id": [ ],
    "comment_count": NumberInt("0"),
    "created_at": "2020-09-09 17:38:51.170000",
    "description": "Managing vague and fuzzy semantic information is a\nchallenging topic in the fields of knowledge engineering and Artificial Intelligence (AI) while there has been some work in the field\nof fuzzy ontologies, there are still many open problems. In this video we briefly overview some advanced features of the management\nof fuzzy ontologies and fuzzy ontology reasoners. Some highlights\npresented here are new algorithms to learn fuzzy ontologies, novel\nreasoning algorithms, new methods to manage imprecise knowledge\nin mobile devices, and the development of real-world applications as\na proof of concept of our developments.",
    "feed_id_list": [ ],
    "foreign_id": "5f59132b4ee80ca4db3510dc",
    "hotspot": NumberInt("5"),
    "hotspotB": NumberInt("5"),
    "liked_count": NumberInt("0"),
    "percentage_watched": null,
    "published_at": NumberLong("1599673612752"),
    "share_count": NumberInt("0"),
    "source": "YouTube download",
    "status": "embedded",
    "subtitles_url": "",
    "tag": [
        "fuzzy Ontologies",
        "fuzzy resoners",
        "gait recognition systems",
        "recomender systems",
        "blockchain smart contracts",
        "Datil",
        "Fudge",
        "learning",
        "fuzzyDL",
        "reasoning",
        "real-world applications"
    ],
    "thumbnail_origin_url": "https://i.ytimg.com/vi/dgftH3E6470/hqdefault.jpg",
    "thumbnail_seo_url": "https://i.ytimg.com/vi/dgftH3E6470/hqdefault.jpg",
    "thumbnail_url": "https://i.ytimg.com/vi/dgftH3E6470/hqdefault.jpg",
    "thumbnails": {
        "default": "https://thumbnail.crossminds.ai/5f59132b4ee80ca4db3510dc/default.png",
        "email": "https://thumbnail.crossminds.ai/5f59132b4ee80ca4db3510dc/email.png",
        "high": "https://thumbnail.crossminds.ai/5f59132b4ee80ca4db3510dc/high.png",
        "max": "https://thumbnail.crossminds.ai/5f59132b4ee80ca4db3510dc/max.png",
        "medium": "https://thumbnail.crossminds.ai/5f59132b4ee80ca4db3510dc/medium.png",
        "standard": "https://thumbnail.crossminds.ai/5f59132b4ee80ca4db3510dc/standard.png"
    },
    "title": "ECAI2020: Advanced Management of Fuzzy Semantic Information",
    "type": "video",
    "ugc": false,
    "updated_at": "2020-09-09 17:46:53.156000",
    "video_length": NumberInt("182"),
    "video_url": "https://www.youtube.com/embed/dgftH3E6470",
    "view_count": NumberInt("29"),
    "watchLater": false,
    "watched": false,
    "video_path": "/crossmind/video/5f59132b4ee80ca4db3510dc/ECAI2020 Advanced Management of Fuzzy Semantic Information.mp4"
}
```

</details>

#### Corssmind中评论信息

主要字段 | 类型 | 说明 |
:-: | :-: | :-: |
target_id| 字符串 | 视频的唯一标识，与foreign_id一致 |
author_name| 字符串 | 评论者名称 |
content| 字典 | key为message的value表示评论内容 |
replys | 字典数组 | 表示此评论的回复 |

<details>

<summary>table_name: crossmind_comment
</summary>

```json
{
    "_id": "5fe1a54ddbed452142eae281",
    "author_avatar": "https://bucket4xmdmvp.s3-us-west-2.amazonaws.com/avatar/default/Dolphin.png",
    "author_id": "axMpxlI0wdQRoBeoV11C9oZmXKC3",
    "author_name": "3040553715",
    "content": {
        "message": "it is nice"
    },
    "created_at": "2020-12-22 07:50:37.207000",
    "dislike_count": NumberInt("0"),
    "is_deleted": false,
    "like_count": NumberInt("0"),
    "ownership_of_comment": false,
    "parent_id": "",
    "reply_count": NumberInt("0"),
    "replys": [ ],
    "root_id": "",
    "target_id": "5f08c80dd8b7c2e383e105b9",
    "target_type": "video",
    "updated_at": "2020-12-22 07:50:37.207000",
    "vote_status": NumberInt("0")
}
```

</details>

#### Corssmind中reaction信息

主要字段 | 类型 | 说明 |
:-: | :-: | :-: |
video_id | 字符串 | 视频的唯一标识，与foreign_id一致 |
message | 字符串 | reaction内容 |
timecode | 浮点数 | 视频的进度，单位/秒 |

<details>

<summary>table_name: crossmind_reaction
</summary>

```json
{
    "_id": "5fe1ac0b18fe84dc0a78ce3f",
    "author": {
        "_id": "5fd8d77c4eba6d1b317c86fd",
        "created_at": "2020-12-15 15:34:20.745000",
        "creator_agreement_accepted_at": null,
        "email": "3040553715@qq.com",
        "email_subscription": {
            "feature_update_subscription": true,
            "notification_email_subscription": true,
            "recommendation_email_subscription": true
        },
        "headline": "",
        "interests": {
            "category": [ ],
            "graph_node": [ ]
        },
        "is_claimed": true,
        "is_editor": false,
        "is_video_author": false,
        "name": "3040553715",
        "photoURL": "https://bucket4xmdmvp.s3-us-west-2.amazonaws.com/avatar/default/Dolphin.png",
        "provider": "",
        "roles": [
            "user"
        ],
        "terms_of_service": true,
        "type": "user",
        "uid": "axMpxlI0wdQRoBeoV11C9oZmXKC3",
        "updated_at": "2020-12-15 15:34:20.745000"
    },
    "author_id": "axMpxlI0wdQRoBeoV11C9oZmXKC3",
    "created_at": "2020-12-22 08:19:23.437000",
    "delete": false,
    "message": "KG is very useful",
    "reaction": { },
    "reply_count": NumberInt("0"),
    "timecode": 25.2440080495911,
    "timestamp": NumberLong("1608625161009"),
    "type": "comment",
    "updated_at": "2020-12-22 08:19:23.437000",
    "video_id": "5f08c80dd8b7c2e383e105b9"
}
```
</details>


#### ACL_Anthology基本信息

   
主要字段 | 类型 | 说明 |
:-: | :-: | :-: |
Anthology ID| 字符串 | 文章的唯一标识 |
title| 字符串 | 文章的标题 |
abstract| 字符串 | 文章的摘要 |
authors| 字符串数组 | 文章的作者 |
Publisher| 字符串 | 文章的出版社 |
DOI| 字符串 | 文章的DOI |
PDF| 字符串 | PDF的url |
PDF_path| 字符串 | PDF的本地路径 |
Video_url| 字符串数组 | 视频url |
Video_path| 字符串数组 | 视频的本地路径 |
slide_path| 字符串数组 | ppt的本地路径 |
Dataset_url| 字符串数组 | 数据集url |
Dataset_path| 字符串数组 | 数据集的本地路径 |
Source_url| 字符串数组 | 源码url |
Source_path| 字符串数组 | 源码的本地路径 |


<details>

<summary> table_name: acl_anthology
</summary>

```json
{
    "_id": ObjectId("5fe53a9b69ad776b9c8e2c1b"),
    "title": "",
    "authors": [
        "Audrey Acken",
        "Dorottya Demszky"
    ],
    "abstract": "In this study, we apply NLP methods to learn about the framing of the 2020 Democratic Presidential candidates in news media. We use both a lexicon-based approach and word embeddings to analyze how candidates are discussed in news sources with different political leanings. Our results show significant differences in the framing of candidates across the news sources along several dimensions, such as sentiment and agency, paving the way for a deeper investigation.",
    "Anthology ID": "2020.winlp-1.32",
    "Volume": "Proceedings of the The Fourth Widening Natural Language Processing Workshop",
    "Volume_url": "/anthology/volumes/2020.winlp-1/",
    "Month": "July",
    "Year": "2020",
    "Address": "Seattle, USA",
    "Publisher": "Association for Computational Linguistics",
    "Pages": "123",
    "URL": "https://www.aclweb.org/anthology/2020.winlp-1.32",
    "URL_url": "https://www.aclweb.org/anthology/2020.winlp-1.32",
    "DOI": "10.18653/v1/2020.winlp-1.32",
    "DOI_url": "http://dx.doi.org/10.18653/v1/2020.winlp-1.32",
    "Video": [
        "http://slideslive.com/38929572"
    ],
    "Video_url": [
        "http://slideslive.com/38929572"
    ],
    "slide_path": [
        "/acl/2020.winlp-1.32/38929572/82b27f65-8995-4e9f-ab50-21a1b5f757c2__0-0016.jpg",
        "/acl/2020.winlp-1.32/38929572/82b27f65-8995-4e9f-ab50-21a1b5f757c2__0-0013.jpg",
        "/acl/2020.winlp-1.32/38929572/82b27f65-8995-4e9f-ab50-21a1b5f757c2__0-0012.jpg",
        "/acl/2020.winlp-1.32/38929572/82b27f65-8995-4e9f-ab50-21a1b5f757c2__0-0011.jpg",
        "/acl/2020.winlp-1.32/38929572/82b27f65-8995-4e9f-ab50-21a1b5f757c2__0-0010.jpg",
        "/acl/2020.winlp-1.32/38929572/82b27f65-8995-4e9f-ab50-21a1b5f757c2__0-0015.jpg",
        "/acl/2020.winlp-1.32/38929572/82b27f65-8995-4e9f-ab50-21a1b5f757c2__0-0014.jpg",
        "/acl/2020.winlp-1.32/38929572/82b27f65-8995-4e9f-ab50-21a1b5f757c2__0-0008.jpg",
        "/acl/2020.winlp-1.32/38929572/82b27f65-8995-4e9f-ab50-21a1b5f757c2__0-0009.jpg",
        "/acl/2020.winlp-1.32/38929572/82b27f65-8995-4e9f-ab50-21a1b5f757c2__0-0004.jpg",
        "/acl/2020.winlp-1.32/38929572/82b27f65-8995-4e9f-ab50-21a1b5f757c2__0-0007.jpg",
        "/acl/2020.winlp-1.32/38929572/82b27f65-8995-4e9f-ab50-21a1b5f757c2__0-0006.jpg",
        "/acl/2020.winlp-1.32/38929572/82b27f65-8995-4e9f-ab50-21a1b5f757c2__0-0005.jpg",
        "/acl/2020.winlp-1.32/38929572/82b27f65-8995-4e9f-ab50-21a1b5f757c2__0-0001.jpg",
        "/acl/2020.winlp-1.32/38929572/82b27f65-8995-4e9f-ab50-21a1b5f757c2__0-0003.jpg"
    ],
    "Video_path": [
        "/acl/2020.winlp-1.32/38929572.mp4"
    ]
}
```

</details>

## 爬虫模块

- 开发语言：python3.6
- 爬虫框架： **Scrapy**
- 系统： Windows
- IDE： VS Code

### Crossmind

    $ scrapy crawl crossmind

#### 视频基本信息

corssmind里视频主要有两种分类方式：按照Category（比如会议等）或按照Knowledge Area。因为前者类数更新要比后者快，所以我们选择根据第二种方式进行遍历。

![avatar](https://github.com/BITCS-Information-Retrieval-2020/crawler-daoerxianqiao/blob/main/extra/pic1.png)

根据api爬取视频基本信息：

    https://api.crossminds.io/web/node/video/name/[1]?limit=[2]&offset=[3]

- [1] 知识领域
- [2] 返回结果数
- [3] 偏移数
  
通过设置这些参数，迭代爬取视频基础信息，包括视频唯一标识foregin_id。随即yield item，并且对foreign_id建立索引，防止重复插入。

#### 评论信息

根据api爬取视频的评论信息：

    https://activity.crossminds.io/comment/target?target_id=[1]&offset=[2]&limit=[3]&target_type=video

- [1] 视频唯一标识
- [2] 偏移数
- [3] 返回结果数

通过设置这些参数，迭代爬取视频的评论信息。

#### reaction信息

根据api爬取视频的reaction信息：

    https://api.crossminds.io/web/reactive/comment/[1]

- [1] 视频唯一标识

通过设置这些参数，迭代爬取视频的reaction信息。

#### PDF文件爬取

在基本信息中，attachment字段中有pdf等信息，这里只把pdf下载到本地中。

<details>

```python
    # 爬取pdf
    for attachment in attachments:
        if attachment['name'] == 'Paper Link':                # arxiv 链接可能直接是pdf 也可能需要进一步修改链接
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
                    pdf_url = pdf_url + attachment['source_link']+ '.pdf'
            pdf_num = len(glob.glob(pathname=self.pdf_base_path + target_id + "/*.pdf"))
            if pdf_num == 0:
                if pdf_url != '':
                    yield scrapy.Request(pdf_url, callback=self.parse_pdf_down,
                            meta={'target_id': target_id}, dont_filter=True)
                else:
                    with open(self.pdf_base_path + 'miss.txt', 'a+') as f:
                        f.write(attachment['source_link'] + '\n')
            break

```

</details>

#### 视频文件爬取

在crossmind中视频url有三类：Youtube、CrossMinds(m3u8)和Vimeo。

##### Youtube

使用pytube工具下载youtube视频（默认下载质量最高的，但不准确，详情见[博客](https://blog.csdn.net/hezhefly/article/details/102531398)）。

         video_path = YouTube(video_url).streams.first()
            .download(dir_path)

##### CrossMinds_m3u8

首先下载m3u8文件，解析出来对应的ts文件列表，逐个下载后，合并成mp4文件。

<details>


```python
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
```
</details>


##### Vimeo

vimeo视频有唯一标识vimeo_id，根据下面的api找到其相关信息，主要有两个重要字段"hls"和"progressive"，前者是m3u8，后者有不同质量的mp4下载链接。我们使用后者下载视频（并选择最低清晰度。。。流量有限）。

        https://player.vimeo.com/video/[1]/config?autopause=1&byline=0\
                            &collections=1&context=Vimeo%5CController%5CClipController.main&default_to_hd=1\
                            &outro=nothing&portrait=0&share=1&title=0&watch_trailer=0

- [1] vimeo视频唯一标识vimeo_id

### ACL_Anthology

       $ scrapy crawl acl_anthology

#### 基本信息

ACL Anthology同样有两种遍历方法：根据页面table爬取或者网站提供的bib压缩包。因为基本是年更，所以我们选择后者，提取bib中的url遍历。


使用xpath爬取每一个页面中的文章标题、文章作者、摘要、pdf等等。唯一标识为Anthology ID，并建立索引。

<details>

```python
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
```

</details>

#### PDF、Dataset、Source等

有的文章会有附件，根据url下载即可（判断是否存在，防止重复下载）。

#### 幻灯片

对于slideslive.com上的视频，还可以爬取ppt。

根据下面api，解析xml，获取幻灯片下载链接:

    https://d2ygwrecguqg66.cloudfront.net/data/presentations/[1]/[1].xml

- [1] 视频id


<details>

```python
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

```

</details>

#### Vimeo

ACL anthology中视频主要有三类：youtube、vimeo和slideslive。

前面两个已叙述过。而slideslive类型本质是vimeo，只不过vimeo_id被隐藏了，根据下面api找到vimeo_id即可按照前面所说的vimeo视频方式下载：

    https://ben.slideslive.com/player/[1]?demo=false

- [1] slideslive中视频id 


## 特别说明

- 我们在视频上做了许多工作，基本两个网站遇到的视频类型都可以下载。
- 为了避免重复插入数据库以及重复下载文件，我们一方面建立索引，一方面进行详尽的判断。所以中断后，也可以直接重新爬取，不会重复下载文件导致速度和流量问题。
- 基于上一点，我们也可以进行增量爬取，特别是crossminds网站。

