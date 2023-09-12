import json

from linebot import LineBotApi
from linebot.models import TextSendMessage

from google.cloud import firestore

import random

def main(request):
    CHANNEL_ACCESS_TOKEN = "(自分のアクセストークン)"
    line_bot_api = LineBotApi(channel_access_token=CHANNEL_ACCESS_TOKEN)
    body = request.get_data(as_text=True)
    body = json.loads(body)
    events = body["events"]
    for event in events:
        if event["type"] == "follow":
            line_bot_api.reply_message(
                reply_token=event["replyToken"],
                messages=TextSendMessage(text="「ヌメロン」と送信して、ゲームを始めましょう！")
            )
            db = firestore.Client()
            doc_ref = db.collection('users').document( event["source"]["userId"] )
            doc_ref.set({
                "is_playing": False,
                "answer": [0, 0, 0],
            })
        else:
            db = firestore.Client()
            doc_ref = db.collection('users').document( event["source"]["userId"] )
            doc = doc_ref.get()
            is_playing = doc.get('is_playing')
            if is_playing:
                # ゲーム中
                call = event["message"]["text"]
                try:    
                    int(call)
                except:
                    rule = False
                if len(call) == 3:
                    if len( set( list(call) ) ) == 3:
                        rule = True
                    else:
                        rule = False
                else:
                    rule = False

                if rule:
                    # 入力ルール○
                    eat = 0
                    bite_test = 0

                    db = firestore.Client()
                    doc_ref = db.collection('users').document( event["source"]["userId"] )
                    doc = doc_ref.get()
                    answer = doc.get('answer')

                    call_num_list_str = list( call )
                    call_num_list_int = [int(call_num_list_str[0]), int(call_num_list_str[1]), int(call_num_list_str[2])]

                    for i in range(3):
                        if answer[i] ==  call_num_list_int[i]:
                            eat = eat + 1
                    
                    for i in range(3):
                        for j in range(3):
                            if answer[i] == call_num_list_int[j]:
                                bite_test += 1
                    bite = bite_test - eat

                    if eat == 3:
                        line_bot_api.reply_message(
                            reply_token=event["replyToken"],
                            messages=TextSendMessage(text="クリア！おめでとう！")
                        )
                        db = firestore.Client()
                        doc_ref = db.collection('users').document( event["source"]["userId"] )
                        doc_ref.set({
                            "is_playing": False,
                            "answer": [0, 0, 0],
                        })
                    else:
                        line_bot_api.reply_message(
                            reply_token=event["replyToken"],
                            messages=TextSendMessage(text=f"EAT:{eat} - BITE:{bite}")
                        )   
                else:
                    # 入力ルール✖️
                    line_bot_api.reply_message(
                        reply_token=event["replyToken"],
                        messages=TextSendMessage(text="重複のない３桁の数字を送ってください！")
                    )   

                pass
            else:
                # ゲーム中でない
                if event["message"]["text"] == "ヌメロン":                    
                    line_bot_api.reply_message(
                        reply_token=event["replyToken"],
                        messages=TextSendMessage(text="重複のない３桁の数字を送ってください！")
                    )         
                    db = firestore.Client()
                    doc_ref = db.collection('users').document( event["source"]["userId"] )
                    num_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                    random.shuffle( num_list )
                    doc_ref.set({
                        "is_playing": True,
                        "answer": [ num_list[0], num_list[1], num_list[2] ],
                    })     
                else:
                    line_bot_api.reply_message(
                        reply_token=event["replyToken"],
                        messages=TextSendMessage(text="「ヌメロン」と送信して、ゲームを始めましょう！")
                    )


    return "ok"




def create_random_number():
    num_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle( num_list )
    return [ num_list[0], num_list[1], num_list[2] ]

print(create_random_number())

def check_input_number():
    call = input()
    try:    
        int(call)
    except:
        return False
    if len(call) == 3:
        if len( set( list(call) ) ) == 3:
            return True
        else:
            return False
    else:
        return False
        
print(check_input_number)

def compare_number(set_num_list, call_num_list, digits=3):
    eat = 0
    bite_test = 0

    for i in range(digits):
        if set_num_list[i] ==  call_num_list[i]:
            eat = eat + 1
    
    for i in range(digits):
        for j in range(digits):
            if set_num_list[i] == call_num_list[j]:
                bite_test += 1
    bite = bite_test - eat
    return eat, bite

print(compare_number([1,2,3], [4,5,6], 3))