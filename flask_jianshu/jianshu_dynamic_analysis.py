from collections import Counter
from datetime import datetime

import jieba
import pymongo
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
        df_lst = []
        for tag in self.en_parent_tags:
            df = pd.DataFrame(self.user_data[tag])
            df_lst.append(df)

        self.df = pd.concat(df_lst)

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

    def get_month_data_pd(self):
        dt_index = pd.to_datetime(list(self.df.time))
        # print(dt_index)
        # print(len(dt_index))
        ts = pd.Series([1] * len(dt_index), index=dt_index)
        # print(ts)
        tsday = ts.resample("1M").sum()
        # print(tsday[tsday > 0].index)
        lstMonth = [x.strftime('%Y-%m') for x in tsday[tsday > 0].index]
        print(lstMonth)
        lst_freq = list(tsday[tsday > 0].values)
        print(lst_freq)

        dic = {}
        dic['month'] = lstMonth
        dic['frequency'] = list(map(int, lst_freq))

        return dic

    def get_day_data_pd(self):
        dt_index = pd.to_datetime(list(self.df.time))
        # print(dt_index)
        # print(len(dt_index))
        ts = pd.Series([1] * len(dt_index), index=dt_index)
        # print(ts)
        tsday = ts.resample("1D").sum()
        # print(tsday[tsday > 0].index)
        lstDay = [x.strftime('%Y-%m-%d') for x in tsday[tsday > 0].index]
        print(lstDay)
        lst_freq = list(tsday[tsday > 0].values)
        print(lst_freq)

        dic = {}
        dic['day'] = lstDay
        dic['frequency'] = list(map(int, lst_freq))

        return dic

    def get_hour_data_pd(self):
        dti = pd.to_datetime(self.df.time).to_frame()
        print(dti)
        dayofweek_group = dti.groupby(dti['time'].map(lambda x: x.hour)).count()

        lst_freq = [int(item) for item in dayofweek_group.values]
        lst_dayofweek = [str(item).rjust(2, '0') + ':00' for item in dayofweek_group.index]

        dic = {}
        dic['hour'] = lst_dayofweek
        dic['frequency'] = lst_freq

        return dic

    def get_week_data_pd(self):
        dti = pd.to_datetime(self.df.time).to_frame()
        print(dti)
        dayofweek_group = dti.groupby(dti['time'].map(lambda x: x.dayofweek)).count()
        week_day_dict = {0: '周一', 1: '周二', 2: '周三', 3: '周四',
                         4: '周五', 5: '周六', 6: '周日', }

        lst_freq = [int(item) for item in dayofweek_group.values]
        lst_dayofweek = [week_day_dict[item] for item in dayofweek_group.index]

        dic = {}
        dic['week'] = lst_dayofweek
        dic['frequency'] = lst_freq

        return dic

    def get_week_hour_data_pd(self):
        dti = pd.to_datetime(self.df.time).to_frame()
        print(dti)
        gg = dti.groupby(
            [dti['time'].map(lambda x: x.dayofweek).rename('dayofweek'),
             dti['time'].map(lambda x: x.hour).rename('hour')])

        g_count = gg.count()

        lst_week_hour_data = []
        max_freq = 0
        for name, grp in gg:
            print(name)  # (周几,几点)
            freq = g_count.loc[name].values[0]  # 频率，次数
            if max_freq < freq:
                max_freq = freq
            tmp_lst = [int(name[0]), int(name[1]), int(freq)]
            lst_week_hour_data.append(tmp_lst)

        dic = {}
        dic['week_hour'] = lst_week_hour_data
        dic['max_freq'] = max_freq

        return dic

    def date_to_week(self, strdate):
        week_day_dict = {0: '0周一', 1: '1周二', 2: '2周三', 3: '3周四',
                         4: '4周五', 5: '5周六', 6: '6周日'}
        timeobj = datetime.strptime(strdate, '%Y-%m-%d %H:%M:%S')
        print(timeobj.weekday())
        return week_day_dict[timeobj.weekday()]

    def date_to_week_other(self, strdate):
        timeobj = datetime.strptime(strdate, '%Y-%m-%d %H:%M:%S')
        print(timeobj.weekday())
        return str(timeobj.weekday())

    def get_comments(self):
        comments = self.user_data['comment_note']
        count = len(self.user_data['comment_note'])
        commentlst = [obj['comment_text'] for obj in comments]
        comment_txt = ''.join(commentlst)
        word_lst = jieba.cut(comment_txt)
        # print(list(word_lst))
        wordlstnew = []
        for w in word_lst:
            if len(w) >= 2:
                wordlstnew.append(w)

        counter = Counter(wordlstnew)
        print(counter.items())
        # [('谢谢', 2), ('分享', 2), ('金山', 1), ('794c', 1), ('可以', 1)]

        lst = []
        for tp in counter.items():
            dic = {
                "name": tp[0],
                "value": tp[1]
            }
            lst.append(dic)

        dic_return = {}
        dic_return['count'] = count
        dic_return['word_cloud'] = lst

        return dic_return