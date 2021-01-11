# with open('./ErQiaoCrawler/ErQiaoCrawler/anthology.bib','r', encoding='utf-8') as f:
#     content_list = f.readlines()
#     contents = [x.strip() for x in content_list]
#     url_list = []
#     for content in contents:
#         if content.startswith('url ='):
#             url_list.append(content[7:-2])
#             with open('./ErQiaoCrawler/ErQiaoCrawler/url_list.txt','a') as f2:
#                 f2.write(content[7:-2]+'\n')

# from pytube import YouTube
# yt = YouTube("https://youtube.com/watch?v=zs0yOpHWBf8")
# print(yt.streams.filter(progressive=True).all())


# 统计数据
# import pymongo
# collection = ['crossmind', 'crossmind_comment', 'crossmind_reaction', 'acl_anthology']

# client = pymongo.MongoClient('mongodb://localhost:27017')
# db = client['daoerxianqiao']

# crossmind = db['crossmind']
# crossmind_comment = db['crossmind_comment']
# crossmind_reaction = db['crossmind_reaction']
# acl_anthology = db['acl_anthology']

# print('crossmind视频基本信息数目：' + str(crossmind.estimated_document_count()))
# print('crossmind视频数目：' + str(crossmind.count_documents({"video_path":{"$ne":None}})))
# print('crossmindPDF数目：' + str(crossmind.count_documents({"pdf_path":{"$ne":None}})))
# print('crossmind_comment数目：' + str(crossmind_comment.estimated_document_count()))
# print('crossmind_reaction数目：' + str(crossmind_reaction.estimated_document_count()))


# print('acl_anthology基本信息数目：' + str(acl_anthology.estimated_document_count()))
# print('acl_anthology视频数目：' + str(acl_anthology.count_documents({"Video_path":{"$ne":None}})))
# print('acl_anthologyPDF视频数目：' + str(acl_anthology.count_documents({"PDF_path":{"$ne":None}})))
# print('acl_anthologyPTT页数目：' + str(acl_anthology.count_documents({"slide_path":{"$ne":None}})))
# print('acl_anthology其他附件数目：' + str(acl_anthology.count_documents({"Dataset_path":{"$ne":None}})+
#                                         acl_anthology.count_documents({"Software_path":{"$ne":None}})+
#                                         acl_anthology.count_documents({"Source_path":{"$ne":None}})))
