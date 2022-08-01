from datetime import timedelta
from doctest import REPORTING_FLAGS
from re import L
import flask
import os
from flask import *
# from mysql.connector import constants
from questionary import password
import requests
import difflib
# import mysql.connector
import random
# from mysql.connector import Error
import time
import base64
from flask_cors import CORS

app = flask.Flask(__name__, static_url_path='/static')
app.secret_key = 'Rasaweb'  # secret_key存session到cookie所需
app.permanent_session_lifetime = timedelta(minutes=270)  # 設定使用者使用時間
CORS(app)
app.config["DEBUG"] = True  # 開啟debug讓我們可以隨時因為程式的變動而更新

Error = 0

##分隔線##-------------------------------------
@app.route('/carbot', methods=['POST'])
def carbot():
    data = request.get_json(silent=True)
    print('data = ', data)
    text=data.get('text')#使用者講話
    user=data.get('user')
    url = 'http://140.125.32.145:5005/webhooks/rest/webhook'
    datajs = {"sender": "bot01", "message": text} #準備送去給RASA的資料
    datajs = json.dumps(datajs)
    x = requests.post(url, data=datajs)  # 傳值到Rasa後回傳
    print("x.json() = ", x.json()) #印出回傳值
    result = x.json()[0]['text'] #將回答的話取出
    print("result = ", result.lower())
    location={
        'Okay, let’s go to the park.':1,
        'okay, let’s go to the park.':1,
        "go to the park":1,
        #################### park ####################
        'What does John do next? Play on the slide, go jogging or build a sand castle?':1,
        'When Mark is playing, he hears a sound from the grass.': 9111,
        'It is a lost puppy.': 9112,
        'The puppy is a yellow dog.': 9113,
        'It has big eyes and ears.': 9113,
        'Mark decides to help it find its owner.': 9113,
        'After a few minutes, Mark sees a man looking around.': 9114,
        'Wow! he is the dog\'s owner.': 9114,
        'In order to thank Mark for his help.': 11,
        'The owner gives him the Badge of Kindness.': 9116,
        'When Jack is jogging, he hears a sound “ai-yo”.': 9121,
        'An old man next to him fall down.': 9122,
        'The old man wears a blue shirt and black pants.': 9123,
        'Jack quickly helps him up.': 12,
        'Luckily, the old man is okay.': 9124,
        'The old man thanked Jack for his help and gives him the Badge of “Little Helper”.': 9125,
        'When Sam is building a sand castle, he sees a lot of garbage in the sandpit.': 9131,
        'Sam goes to clean it up.': 9132,
        'He picks up a trash bag and a paper bag.': 9133,
        'When he is cleaning the sandpit, a woman sees him.': 13,
        'She thinks Sam is a good kid so she gives him the Badge of “Nature-lover”.': 9135,


        #################### restaurant ####################
        'Okay, let’s go to the restaurant.':2,
        'Okay, let’s go to the restaurant.':2,
        "go to the restaurant":2,
        'What does he do next? Eat hamburger, bento, or Ramen?':2,
        "After Tony sits down, he sees a wallet on the seat.":9211,
        "The wallet is red and long.":9212,
        "Tony brings the wallet to the counter.":9213,
        "A man standing at the counter says.":21,
        "That is my wallet! You found it! Thank you!":9214,
        "The man gives Tony  the Badge of Honesty to thank him.":9215,
        "Right in front of the Lunch box shop, Tony sees a homeless man walking around.":9221,
        "The man is tall and skinny.":9222,
        "After finding out the homeless man did no eat anything for days,":9222,
        "Tony buys a lunch box for him.":9223,
        "The man is very happy.":22,
        "He thanks Tony for helping him,":9224,
        "so he gives Tony the Badge of Goodwill.":9225,
        "In the Ramen shop, a staff spilled the Ramen on the floor.":9231,
        "The soup and noodle are all on the floor.":9232,
        "It is good that no one is hurt.":9232,
        "Tony gets up from his seat and helps the staff to clean the floor.":9233,
        "The staff is thankful of Tony’s help,":23,
        "and decided to give Tony the Badge of Kindness.":9235,


        #################### supermarket ####################
        'Okay, let’s go to the supermarket.':3,
        'Okay, let’s go to the supermarket.':3,
        "go to the supermarket":3,
        'What does he do next? Buy daily goods, snacks or drinks?':3,
        'At the daily goods shelf,':9311,
        'Tom sees a salesman moving boxes into the storehouse.':9311,
        'She has a lot of boxed in her hands.':9311,
        '“Oh-O”! One small box falls off from her hands.':9312,
        'The salesman can not pick it up.':9313,
        'So Tom helps her pick up the small box.':31,
        'The salesman thanks Tom for his help so she gave Tom the Badge of \'Little helper\'.':9314,
        
        'At the snack shelf,':9321,
        'Tom sees a man looking around for something.':9321,
        'The man wants potato chips and chocolate but he can not find them.':9322,
        'Tom helps him to find the snacks.':9323,
        'The man shows a big smile on his face after finding the snacks he wants.':32,
        'He want to thank Tom for his help, so he gives Tom the Badge of “Kindness”.':9324,
        'At the drinks shelf,':9331,
        'Tom sees a boy crying.':9332,
        'The boy wears a green t-shirt and blue pants.':9332,
        'He is very sad and wants to see his mom.':9333,
        'Tom takes the boy to the service counter.':9334,
        'The boy’s Mom is waiting there.':33,
        'The boy runs to his mom right away.':9335,
        'The boy’s family is happy and thanks Tom.':9335,
        'They give Tom “the Badge of Superhero”.':9336,
        
        "Good job! You are finish the park story. Let's go home!":111,
        "Good job! You are finish the restaurant story. Let's go home!":222,
        "Good job! You are finish the supermarket story. Let's go home!":333
    }
    try:
        if result in location:
            datajs={
            "respond":result,
            "target":location[result]
            }
            print("text = " , text)
        else:
            print('not exist')
    except TypeError as e:
        print("資料庫連接失敗：", e)
        # print("資料庫連接失敗：", e.code)
        # print("datajs = " , datajs)

    # finally:
    #     if (mydb.is_connected()):
    #         mycursor.close()
    #         mydb.close()
    #         print("資料庫關閉")
    return datajs



if __name__ == "__main__":
    r_animal = random.randint(0, 19)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
 
