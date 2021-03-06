from pprint import pprint

import pymongo
import re
import sys
from flask import Flask, render_template, request, redirect, url_for

from flask_jianshu.jianshu_dynamic_analysis import AnalysisUser
from flask_jianshu.jianshu_dynamic_spider import JianshuSpider

sys.setrecursionlimit(6000)
app=Flask(__name__)

client = pymongo.MongoClient(host='localhost')
db = client['JianShu']

@app.route('/',methods=['POST','GET'])
def home():
    if request.method=='POST':
        url=request.form['url']
        match_result=re.match(r'(https://)?(www.jianshu.com/u/)?(\w{12}|\w{6})$',url)
        if match_result:
            slug=match_result.groups()[-1]
            return redirect(url_for('jianshu_timeline',slug=slug))
        else:
            return render_template('index.html',error_msg='输入错误！')
        # print(url)
    return render_template('index.html')

def get_user_dynamic_info(slug):
    js = JianshuSpider(slug)
    js.get_lastest_time()
    item = js.get_base_info()
    pprint(item)
    js.get_user_timeline(None, 1)
    print('采集所有动态完毕')
    pprint(js.timeline)
    all_user_info = dict(item, **js.timeline)
    if 'join_time' in js.timeline:
        js.add_user_timeline_to_mongodb(all_user_info)
    else:
        js.append_user_timeline_to_mongodb()


@app.route('/timeline')
def jianshu_timeline():
    slug=request.args.get('slug')
    # 采集用户全部动态并保存到mongodb
    get_user_dynamic_info(slug)
    au = AnalysisUser(slug)
    user_base_info = au.get_user_base_info()
    first_info=au.get_first_info()
    tags_data = au.get_tags_data()

    month_data_dic = au.get_month_data_pd()
    day_data_dic = au.get_day_data_pd()
    hour_data_dic = au.get_hour_data_pd()
    week_data_dic = au.get_week_data_pd()
    week_hour_dic = au.get_week_hour_data_pd()

    word_count_dic = au.get_comments()
    return render_template('timeline.html',
                           baseinfo=user_base_info,
                           first_tag_time=first_info,
                           tags_data=tags_data,
                           month_data_dic = month_data_dic,
                           day_data_dic=day_data_dic,
                           hour_data_dic=hour_data_dic,
                           week_data_dic=week_data_dic,
                           week_hour_dic=week_hour_dic,
                           word_count_dic=word_count_dic
                           )
if __name__ == '__main__':
    # slug = '2c0dd7ae8db2'
    app.run()

