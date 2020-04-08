import re

from flask import Flask, render_template, request

app=Flask(__name__)

@app.route('/',methods=['POST','GET'])
def home():
    if request.method=='POST':
        url=request.form['url']
        match_result=re.match(r'(https://)?(www.jianshu.com/u/)?(\w{12}|\w{6})$',url)
        if match_result:
            slug=match_result.groups()[-1]
            print(slug)
        else:
            return render_template('index.html',error_msg='输入错误！')
        print(url)
    return render_template('index.html')





if __name__ == '__main__':
    app.run()

