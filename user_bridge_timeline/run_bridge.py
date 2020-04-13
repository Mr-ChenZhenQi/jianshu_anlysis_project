from pprint import pprint

import pymongo
import sys

from user_bridge_timeline.User_bridge_timelineSpider import User_bridge_timelineSpider

sys.setrecursionlimit(1000)
class User_bridge_timeline:
    def __init__(self):
        self.client = pymongo.MongoClient(host='localhost')
        self.db = self.client['JianShu']
        self.userid_info=self.db.user

    def get_user_id(self):
        result=self.userid_info.find().sort("slug ",pymongo.ASCENDING)
        slug_lst=[]
        for i in result:
            slug_lst.append(i['slug'])
        self.save_user_time_line(slug_lst,num=0)

    def save_user_time_line(self,slug_lst,num):
        if len(slug_lst)>num:
            ubt=User_bridge_timelineSpider(slug_lst[num])
            ubt.get_lastest_time()
            item = ubt.get_base_info()
            ubt.get_user_timeline(None, 1)
            print('采集所有动态完毕')
            all_user_info = dict(item, **ubt.timeline)
            if 'join_time' in ubt.timeline:
                ubt.add_user_timeline_to_mongodb(all_user_info)
            else:
                ubt.append_user_timeline_to_mongodb()

            self.save_user_time_line(slug_lst,num+1)
        else:
            pass
if __name__ == '__main__':
    print('程序开始啦！！')
    u=User_bridge_timeline()
    u.get_user_id()
