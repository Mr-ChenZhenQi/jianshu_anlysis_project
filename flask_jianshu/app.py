import re
from pprint import pprint

import requests
from fake_useragent import UserAgent
from flask import Flask, render_template, request, redirect, url_for
from lxml import etree

app=Flask(__name__)

@app.route('/',methods=['POST','GET'])
def home():
    if request.method=='POST':
        url=request.form['url']
        match_result=re.match(r'(https://)?(www.jianshu.com/u/)?(\w{12}|\w{6})$',url)
        if match_result:
            slug=match_result.groups()[-1]
            # print(slug)
            return redirect(url_for('jianshu_timeline',slug=slug))
        else:
            return render_template('index.html',error_msg='输入错误！')
        print(url)
    return render_template('index.html')



BASE_HEADERS = {
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
    'Host': 'www.jianshu.com',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'X-Requested-With': 'XMLHttpRequest',
    'Accept': 'text/html, */*; q=0.01',
    'User-Agent': UserAgent().random,
    'Connection': 'keep-alive',
    'Referer': 'http://www.jianshu.com',
}

timeline = {
    'comment_note': [],
    'like_note': [],
    'reward_note': [],
    'share_note': [],
    'like_user': [],
    'like_collection': [],
    'like_comment': [],
    'like_notebook': [],
}

join_jianshu_time = ''

def jianshu_timeline(slug,maxid,page):
    global join_jianshu_time
    AJAX_HEADERS = {"Referer": f"https//:www.jianshu.com/u/{slug}",
                    "X-PJAX": "true"}
    headers = dict(BASE_HEADERS, **AJAX_HEADERS)

    print(f'爬取第{page}页动态')

    if maxid==None:
        url = f'http://www.jianshu.com/users/{slug}/timeline'
    else:
        url=f'https://www.jianshu.com/users/{slug}/timeline?max_id={maxid}&page={page}'

    respont= requests.get(url=url,headers=headers)
    tree=etree.HTML(respont.text)
    lis=tree.xpath('.//li')
    last_li_id=lis[-1].xpath('@id')[0].replace('feed-','')
    maxid=int(last_li_id)-1
    if lis:
        for li in lis:
            type=li.xpath('.//@data-type')[0]
            time=li.xpath('.//@data-datetime')[0].replace('T','').replace('+08:00','')
            if type =='join_jianshu':
                join_jianshu_time=time
                return
            timeline[type].append(time)
        pprint(timeline)

    jianshu_timeline(slug,maxid,page+1)



if __name__ == '__main__':
    slug = '8b23f6864f5d'
    jianshu_timeline(slug,None,1)
    # app.run()

