from collections import Counter

import pymongo
import numpy as np
import pandas as pd

class AnalysisUser:
    def __init__(self,slug):
        self.client = pymongo.MongoClient(host='localhost')
        self.db = self.client['JianShu']
        self.slug = slug
        self.user_data = self.db['user_timeline'].find_one({'slug': self.slug})
        self.zh_parent_tags = ['发表评论', '喜欢文章', '赞赏文章', '发表文章', '关注用户', '关注专题', '点赞评论', '关注文集']
        self.en_parent_tags = ['comment_note', 'like_note', 'reward_note', 'share_note', 'like_user', 'like_collection',
                           'like_comment', 'like_notebook']
    def get_user_base_info(self):
        baseinfo = {'head_pic': self.user_data['head_pic'],
                    'nickname': self.user_data['nickname'],
                    'update_time': self.user_data['update_time'],
                    'like_users_num': self.user_data['following_num'],
                    'followers_num': self.user_data['followers_num'],
                    'share_notes_num': self.user_data['articles_num'],
                    'words_num': self.user_data['words_num'],
                    'be_liked_num': self.user_data['be_liked_num'],
                    'like_notes_num': len(self.user_data['like_note']),
                    'like_colls_num': len(self.user_data['like_collection']),
                    'like_nbs_num': len(self.user_data['like_notebook']),
                    'comment_notes_num': len(self.user_data['comment_note']),
                    'like_comments_num': len(self.user_data['like_comment']),
                    'reward_notes_num': len(self.user_data['reward_note'])
                    }
        # print(baseinfo)
        return baseinfo

    def extract_first_tag_time(self,data_list):
        if len(data_list) > 0:
            sorted_lst = sorted(data_list, key=lambda obj: obj['time'])
            first_element = sorted_lst[0]
            return first_element
        else:
            return None

    def get_first_info(self):
        first_tag_time={
            'join_time':self.user_data['join_time'],
            'first_like_user': self.extract_first_tag_time(self.user_data['like_user']),
            'first_share_note': self.extract_first_tag_time(self.user_data['share_note']),
            'first_like_note': self.extract_first_tag_time(self.user_data['like_note']),
            'first_like_coll': self.extract_first_tag_time(self.user_data['like_collection']),
            'first_like_nb': self.extract_first_tag_time(self.user_data['like_notebook']),
            'first_comment': self.extract_first_tag_time(self.user_data['comment_note']),
            'first_like_comment': self.extract_first_tag_time(self.user_data['like_comment']),
            'first_reward_note': self.extract_first_tag_time(self.user_data['reward_note']),
        }
        return first_tag_time
    def get_tags_data(self):
        tags_zh_name_lst=[{'name':zh_name} for zh_name in self.zh_parent_tags]
        tags_values=[{'value':len(self.user_data[tag])} for tag in self.en_parent_tags]
        tags_data=[dict(tags_zh_name_lst[i],**tags_values[i]) for i in range(len(tags_values))]
        return tags_data

    def get_month_data(self):
        all_time_lst = []
        for type in self.en_parent_tags:
            type_lst = [obj['time'][0:7] for obj in self.user_data[type]]
            all_time_lst.extend(type_lst)

        # print(all_time_lst)
        # print(len(all_time_lst))
        counter = Counter(all_time_lst)
        # print(counter.items())
        sorted_lst = sorted(counter.items(), key=lambda x: x[0])
        month_lst = [item[0] for item in sorted_lst]
        frequency_lst = [item[1] for item in sorted_lst]

        dic = {}
        dic['month'] = month_lst
        dic['frequency'] = frequency_lst

        return dic

    def get_day_data(self):
        all_time_lst = []
        for type in self.en_parent_tags:
            type_lst = [obj['time'][0:10] for obj in self.user_data[type]]
            all_time_lst.extend(type_lst)

        # print(all_time_lst)
        # print(len(all_time_lst))
        counter = Counter(all_time_lst)
        # print(counter.items())
        sorted_lst = sorted(counter.items(), key=lambda x: x[0])
        month_lst = [item[0] for item in sorted_lst]
        frequency_lst = [item[1] for item in sorted_lst]

        dic = {}
        dic['day'] = month_lst
        dic['frequency'] = frequency_lst

        return dic

    def get_hour_data(self):
        all_time_lst = []
        for type in self.en_parent_tags:
            type_lst = [obj['time'][11:13] for obj in self.user_data[type]]
            all_time_lst.extend(type_lst)

        # print(all_time_lst)
        # print(len(all_time_lst))
        counter = Counter(all_time_lst)
        # print(counter.items())
        sorted_lst = sorted(counter.items(), key=lambda x: x[0])
        month_lst = [item[0] for item in sorted_lst]
        frequency_lst = [item[1] for item in sorted_lst]

        dic = {}
        dic['hour'] = month_lst
        dic['frequency'] = frequency_lst

        return dic





