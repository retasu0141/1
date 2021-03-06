from flask import Flask, request, abort,render_template
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, JoinEvent, TextMessage, TextSendMessage, FlexSendMessage,  PostbackEvent, TemplateSendMessage,ButtonsTemplate,URIAction,QuickReplyButton,QuickReply
)

import time
import math
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

import psycopg2
import random

from datetime import datetime as dt

import urllib.request, urllib.error

from apiclient.discovery import build
import urllib.parse
import re, requests
app = Flask(__name__)

set = {}

def syoukai():
    data = {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://live.staticflickr.com/65535/50834110728_1395d79f76_n.jpg",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
          "type": "uri",
          "uri": "http://linecorp.com/"
        }
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "Editor‘s Camp",
            "weight": "bold",
            "size": "xl",
            "align": "center"
          },
          {
            "type": "text",
            "text": "受付へようこそ！",
            "weight": "bold",
            "size": "xl",
            "align": "center"
          },
          {
            "type": "text",
            "text": "ここでは以下のことを行います",
            "weight": "bold",
            "size": "md",
            "align": "center",
            "margin": "md"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "参加ルールの説明",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "center"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "自分のTwitterの登録",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center",
                "margin": "none"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "動画編集歴の登録",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "自分のこれからの目標の登録",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "悩み事アンケート",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "参加後ノートに作成する自己紹介文配布",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "動画編集者の森へ招待！",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          },
          {
            "type": "text",
            "text": "下のボタンを押して次に進もう！",
            "weight": "bold",
            "size": "md",
            "align": "center",
            "margin": "md"
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
              "type": "postback",
              "label": "参加ルールを聞く",
              "data": "注意事項",
              "displayText": "参加ルールを教えて！"
            }
          },
          {
            "type": "spacer",
            "size": "sm"
          }
        ],
        "flex": 0
      }
    }
    return data

def attention():
    data = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://cdn.pixabay.com/photo/2015/02/13/10/18/stop-634941_1280.jpg",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "参加ルールの説明",
        "weight": "bold",
        "size": "xl",
        "align": "center"
      },
      {
        "type": "text",
        "text": "ルールはたったの二つだけです！",
        "weight": "bold",
        "size": "md",
        "align": "center",
        "margin": "md"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "1.",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "Twitterのアカウント名で参加する。",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "2.",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "モラルに反する発言をしない。",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          }
        ]
      },
      {
        "type": "text",
        "text": "以上の二つを守れる方は",
        "weight": "bold",
        "size": "md",
        "align": "center",
        "margin": "md"
      },
      {
        "type": "text",
        "text": "次に進んで下さい",
        "weight": "bold",
        "size": "md",
        "align": "center",
        "margin": "none"
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "postback",
          "label": "Twitterの登録",
          "data": "twitter",
          "displayText": "Twitterの登録をするよ！"
        }
      },
      {
        "type": "spacer",
        "size": "sm"
      }
    ],
    "flex": 0
  }
}
    return data

def twitter():
    data = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://cdn.pixabay.com/photo/2018/05/08/08/42/handshake-3382503_1280.jpg",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "Twitterの登録",
        "weight": "bold",
        "size": "xl",
        "align": "center"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "・あつまれ動画編集の森では信頼を大切にしています。",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "start"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "・信頼関係を築く為、Twitter名での参加がルールとなっています。",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "start"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "start",
                "text": "・この後自己紹介用のテンプレートを配布するにあたって自分のTwitter情報を登録して頂きます。"
              }
            ]
          }
        ]
      },
      {
        "type": "text",
        "text": "つまり自分のTwitterアカウントの",
        "weight": "bold",
        "size": "md",
        "align": "center",
        "margin": "md"
      },
      {
        "type": "text",
        "text": "[リンク]or[id]",
        "weight": "bold",
        "size": "md",
        "align": "center",
        "margin": "none"
      },
      {
        "type": "text",
        "text": "を送信して頂きます",
        "weight": "bold",
        "size": "md",
        "align": "center",
        "margin": "none"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "[Twitterリンク例]",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "https://twitter.com/retasu_0141",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "[Twitter id例]",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "@retasu_0141",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          }
        ]
      },
      {
        "type": "text",
        "text": "上の二つの例を参考に",
        "weight": "bold",
        "size": "xs",
        "align": "center",
        "margin": "md"
      },
      {
        "type": "text",
        "text": "自分のTwitter情報を送信してください！",
        "weight": "bold",
        "size": "xs",
        "align": "center",
        "margin": "none"
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "spacer",
        "size": "sm"
      }
    ],
    "flex": 0
  }
}
    return data

def data1(twitter):
    data = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://cdn.pixabay.com/photo/2018/06/12/15/08/question-mark-3470783_1280.jpg",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "Twitter登録の確認",
        "weight": "bold",
        "size": "xl",
        "align": "center"
      },
      {
        "type": "text",
        "text": "Twitter情報は以下の内容で大丈夫ですか？",
        "weight": "bold",
        "size": "xs",
        "align": "center",
        "margin": "md"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": twitter,
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "postback",
          "label": "はい",
          "data": "ok",
          "displayText": "OK!"
        }
      },
      {
        "type": "button",
        "style": "secondary",
        "height": "sm",
        "action": {
          "type": "postback",
          "label": "いいえ",
          "data": "no",
          "displayText": "もう一度設定！"
        }
      },
      {
        "type": "spacer",
        "size": "sm"
      }
    ],
    "flex": 0
  }
}
    return data

def data2():
    data = {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://cdn.pixabay.com/photo/2016/01/15/12/02/editing-1141505_1280.jpg",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
          "type": "uri",
          "uri": "http://linecorp.com/"
        }
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "動画編集歴の登録",
            "weight": "bold",
            "size": "xl",
            "align": "center"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "start",
                    "text": "・この後自己紹介用のテンプレートを配布するにあたって自分の動画編集歴を登録して頂きます。"
                  }
                ]
              },
              {
                "type": "text",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "start",
                "text": "・動画編集でなくても活動履歴などを書いて頂いて結構です"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "[動画編集歴 例]",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "2020年6月辺りから",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "ゲーム実況を2019年辺りから",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "最近始めたばかり",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "center"
                  }
                ]
              }
            ]
          },
          {
            "type": "text",
            "text": "上の例を参考に",
            "weight": "bold",
            "size": "xs",
            "align": "center",
            "margin": "md"
          },
          {
            "type": "text",
            "text": "自分の動画編集歴を送信してください！",
            "weight": "bold",
            "size": "xs",
            "align": "center",
            "margin": "none"
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "spacer",
            "size": "sm"
          }
        ],
        "flex": 0
      }
    }
    return data

def data3(data_):
    data = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://cdn.pixabay.com/photo/2018/06/12/15/08/question-mark-3470783_1280.jpg",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "動画編集歴登録の確認",
        "weight": "bold",
        "size": "xl",
        "align": "center"
      },
      {
        "type": "text",
        "text": "動画編集歴は以下の内容で大丈夫ですか？",
        "weight": "bold",
        "size": "xs",
        "align": "center",
        "margin": "md"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": data_,
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "postback",
          "label": "はい",
          "data": "ok2",
          "displayText": "OK!"
        }
      },
      {
        "type": "button",
        "style": "secondary",
        "height": "sm",
        "action": {
          "type": "postback",
          "label": "いいえ",
          "data": "no2",
          "displayText": "もう一度設定！"
        }
      },
      {
        "type": "spacer",
        "size": "sm"
      }
    ],
    "flex": 0
  }
}
    return data

def data4():
    data = {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://cdn.pixabay.com/photo/2016/03/09/09/43/person-1245959_1280.jpg",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
          "type": "uri",
          "uri": "http://linecorp.com/"
        }
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "目標の登録",
            "weight": "bold",
            "size": "xl",
            "align": "center"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "start",
                    "text": "・この後自己紹介用のテンプレートを配布するにあたって自分の目標を登録して頂きます。"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "[目標 例]",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "案件を獲得する！",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "人脈を増やしたい！",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "まずは編集を経験してみたい！",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "center"
                  }
                ]
              }
            ]
          },
          {
            "type": "text",
            "text": "上の例を参考に",
            "weight": "bold",
            "size": "xs",
            "align": "center",
            "margin": "md"
          },
          {
            "type": "text",
            "text": "自分の目標を送信してください！",
            "weight": "bold",
            "size": "xs",
            "align": "center",
            "margin": "none"
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "spacer",
            "size": "sm"
          }
        ],
        "flex": 0
      }
    }
    return data

def data5(text):
    data = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://cdn.pixabay.com/photo/2016/01/19/17/53/writing-1149962_1280.jpg",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "自己紹介テンプレート配布",
        "weight": "bold",
        "size": "lg",
        "align": "center"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "下のボタンからテンプレートを受け取れるので、テンプレートを元に参加後オープンチャットのノートに自己紹介を書き込んで下さい！",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "postback",
          "label": "受け取る",
          "data": "受け取る",
          "displayText": text
        }
      },
      {
        "type": "spacer",
        "size": "sm"
      }
    ],
    "flex": 0
  }
}
    return data

def data6():
    data = {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://cdn.pixabay.com/photo/2016/10/24/23/11/doors-1767562_1280.jpg",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
          "type": "uri",
          "uri": "http://linecorp.com/"
        }
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "さあ、参加しよう！",
            "weight": "bold",
            "size": "xl",
            "align": "center"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "登録おつかれ様でした！",
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "center"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "下のボタンから参加しましょう！",
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          },
          {
            "type": "text",
            "text": "参加後自己紹介文をノートに貼ろう！",
            "weight": "bold",
            "size": "sm",
            "align": "center",
            "margin": "sm"
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
              "type": "uri",
              "label": "参加！",
              "uri": "https://line.me/ti/g2/lDVbXX6utEKgPM-QB3tylA?utm_source=invitation&amp;utm_medium=link_copy&amp;utm_campaign=default"
            }
          },
          {
            "type": "spacer",
            "size": "sm"
          }
        ],
        "flex": 0
      }
    }
    return data

def data7(text):
    data = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://cdn.pixabay.com/photo/2018/06/12/15/08/question-mark-3470783_1280.jpg",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "目標登録の確認",
        "weight": "bold",
        "size": "xl",
        "align": "center"
      },
      {
        "type": "text",
        "text": "目標は以下の内容で大丈夫ですか？",
        "weight": "bold",
        "size": "xs",
        "align": "center",
        "margin": "md"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": text,
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "postback",
          "label": "はい",
          "data": "ok3",
          "displayText": "OK!"
        }
      },
      {
        "type": "button",
        "style": "secondary",
        "height": "sm",
        "action": {
          "type": "postback",
          "label": "いいえ",
          "data": "no3",
          "displayText": "もう一度設定！"
        }
      },
      {
        "type": "spacer",
        "size": "sm"
      }
    ],
    "flex": 0
  }
}
    return data

def data8():
    data = {
      "type": "carousel",
      "contents": [
        {
          "type": "bubble",
          "hero": {
            "type": "image",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "url": "https://cdn.pixabay.com/photo/2017/05/02/10/01/checklist-2277702_1280.jpg"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "アンケート",
                "wrap": True,
                "weight": "bold",
                "size": "xxl",
                "align": "center"
              },
              {
                "type": "text",
                "text": "にご協力ください！",
                "wrap": True,
                "weight": "bold",
                "size": "xl",
                "align": "center"
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "右にある4つの悩みのうち",
                    "wrap": True,
                    "weight": "bold",
                    "size": "xs",
                    "align": "center",
                    "margin": "none"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "wrap": True,
                    "weight": "bold",
                    "size": "xs",
                    "align": "center",
                    "text": "自分に当てはまるものを選択してください！"
                  }
                ]
              }
            ]
          },
          "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "image",
                "url": "https://charbase.com/images/glyph/10137",
                "size": "lg",
                "aspectMode": "cover"
              }
            ]
          }
        },
        {
          "type": "bubble",
          "hero": {
            "type": "image",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "url": "https://cdn.pixabay.com/photo/2016/01/31/20/20/frightened-1172122_1280.jpg"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "今の編集スキルで",
                "wrap": True,
                "weight": "bold",
                "size": "xl",
                "align": "center"
              },
              {
                "type": "text",
                "text": "案件を最後までこなせるか不安...",
                "wrap": True,
                "weight": "bold",
                "size": "md",
                "align": "center"
              }
            ]
          },
          "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "image",
                "url": "https://static.thenounproject.com/png/76988-200.png",
                "size": "lg",
                "aspectMode": "cover"
              },
              {
                "type": "button",
                "style": "primary",
                "action": {
                  "type": "postback",
                  "label": "これを選ぶ",
                  "data": "1",
                  "displayText": "1番目を選んだよ！"
                }
              }
            ]
          }
        },
        {
          "type": "bubble",
          "hero": {
            "type": "image",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "url": "https://cdn.pixabay.com/photo/2020/08/31/00/29/man-5531026_1280.jpg"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "実績がないから",
                "wrap": True,
                "weight": "bold",
                "size": "xl",
                "align": "center"
              },
              {
                "type": "text",
                "text": "クラウドソーシングに応募しても",
                "wrap": True,
                "weight": "bold",
                "size": "md",
                "align": "center"
              },
              {
                "type": "text",
                "text": "なかなか案件を獲得できない...",
                "wrap": True,
                "weight": "bold",
                "size": "md",
                "align": "center"
              }
            ]
          },
          "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "image",
                "url": "https://static.thenounproject.com/png/76988-200.png",
                "size": "lg",
                "aspectMode": "cover"
              },
              {
                "type": "button",
                "style": "primary",
                "action": {
                  "type": "postback",
                  "label": "これを選ぶ",
                  "data": "2",
                  "displayText": "2番目を選んだよ！"
                }
              }
            ]
          }
        },
        {
          "type": "bubble",
          "hero": {
            "type": "image",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "url": "https://cdn.pixabay.com/photo/2014/07/12/14/55/bus-stop-391242_1280.jpg"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "営業文の",
                "wrap": True,
                "weight": "bold",
                "size": "xl",
                "align": "center"
              },
              {
                "type": "text",
                "text": "書き方がわからない...",
                "wrap": True,
                "weight": "bold",
                "size": "md",
                "align": "center"
              }
            ]
          },
          "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "image",
                "url": "https://static.thenounproject.com/png/76988-200.png",
                "size": "lg",
                "aspectMode": "cover"
              },
              {
                "type": "button",
                "style": "primary",
                "action": {
                  "type": "postback",
                  "label": "これを選ぶ",
                  "data": "3",
                  "displayText": "3番目を選んだよ！"
                }
              }
            ]
          }
        },
        {
          "type": "bubble",
          "hero": {
            "type": "image",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "url": "https://cdn.pixabay.com/photo/2017/08/25/21/46/upset-2681502_1280.jpg"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "発注者と",
                "wrap": True,
                "weight": "bold",
                "size": "xl",
                "align": "center"
              },
              {
                "type": "text",
                "text": "上手くコミュニケーションが",
                "wrap": True,
                "weight": "bold",
                "size": "md",
                "align": "center"
              },
              {
                "type": "text",
                "text": "取れるか心配...",
                "wrap": True,
                "weight": "bold",
                "size": "md",
                "align": "center"
              }
            ]
          },
          "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "image",
                "url": "https://static.thenounproject.com/png/76988-200.png",
                "size": "lg",
                "aspectMode": "cover"
              },
              {
                "type": "button",
                "style": "primary",
                "action": {
                  "type": "postback",
                  "label": "これを選ぶ",
                  "data": "4",
                  "displayText": "4番目を選んだよ！"
                }
              }
            ]
          }
        }
      ]
    }
    return data

def text(user_id):
    data = '名前:自分の名前を入力\n自分のTwitter:{twitter}\n動画編集歴:{d_n}\nこれからの目標:{d_t}\nポートフォリオのURL:\nみんなへ一言:'.format(twitter=set[user_id]['twitter'],d_n=set[user_id]['d_n'],d_t=set[user_id]['d_t'])
    return data

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/")
def hello_world():
    return "hello world!"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
'''@handler.add(JoinEvent)
def join(event):
    reply_token = event.reply_token
    data = syoukai()
    flex = {"type": "flex","altText": "自己紹介","contents":data}
    container_obj = FlexSendMessage.new_from_json_dict(flex)
    line_bot_api.reply_message(reply_token,messages=container_obj)'''


@handler.add(PostbackEvent)
def on_postback(event):
    reply_token = event.reply_token
    user_id = event.source.user_id
    postback_msg = event.postback.data

    if "注意事項" in postback_msg and user_id == set[user_id]['user_id'] and set[user_id]['n'] == 1:
        set[user_id]['n'] = 2
        data = attention()
        flex = {"type": "flex","altText": "注意事項","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

    if "twitter" in postback_msg and user_id == set[user_id]['user_id'] and set[user_id]['n'] == 2:
        set[user_id]['n'] = 3
        data = twitter()
        flex = {"type": "flex","altText": "twitter登録","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

    if "no" in postback_msg and user_id == set[user_id]['user_id'] and set[user_id]['n'] == 4:
        set[user_id]['n'] = 3
        data = twitter()
        flex = {"type": "flex","altText": "twitter登録","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

    if "ok" in postback_msg and user_id == set[user_id]['user_id'] and set[user_id]['n'] == 4:
        set[user_id]['n'] = 5
        data = data2()
        flex = {"type": "flex","altText": "動画編集歴","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

    if "no2" in postback_msg and user_id == set[user_id]['user_id'] and set[user_id]['n'] == 6:
        set[user_id]['n'] = 5
        data = data2()
        flex = {"type": "flex","altText": "twitter登録","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

    if "ok2" in postback_msg and user_id == set[user_id]['user_id'] and set[user_id]['n'] == 6:
        set[user_id]['n'] = 7
        data = data4()
        flex = {"type": "flex","altText": "目標","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

    if "no3" in postback_msg and user_id == set[user_id]['user_id'] and set[user_id]['n'] == 8:
        set[user_id]['n'] = 7
        data = data4()
        flex = {"type": "flex","altText": "twitter登録","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

    if "ok3" in postback_msg and user_id == set[user_id]['user_id'] and set[user_id]['n'] == 8:
        set[user_id]['n'] = 9
        data = data8()
        flex = {"type": "flex","altText": "アンケート","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

    if postback_msg in ['1','2','3','4'] and user_id == set[user_id]['user_id'] and set[user_id]['n'] == 9:
        set[user_id]['n'] = 10
        text_ = text(user_id)
        q = postback_msg
        line_bot_api.multicast(['U76d18383a9b659b9ab3d0e43d06c1e78','U6884dfdb4c4091381363d84965956f2f'],TextSendMessage(text='誰かが参加しようとしています！\n[詳細]\nTwitter:{twitter}\n動画編集歴:{d_n}\n目標:{d_t}\n悩み:{q}'.format(twitter=set[user_id]['twitter'],d_n=set[user_id]['d_n'],d_t=set[user_id]['d_t'],q=q)))
        data = data5(text_)
        flex = {"type": "flex","altText": "テンプレート配布","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

    if "受け取る" in postback_msg and user_id == set[user_id]['user_id'] and set[user_id]['n'] == 10:
        data = data6()
        flex = {"type": "flex","altText": "入ろう！","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)




@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global set_
    global stoptime
    global stoppoint
    msg_from = event.reply_token
    msg_text = event.message.text
    msg_id = event.message.id
    user_id = event.source.user_id

    if msg_text == 'Editor‘s Campに入る':
        data = syoukai()
        set[user_id] = {'user_id':user_id,'n':1,'twitter':'','d_n':'','d_t':'','text':''}
        flex = {"type": "flex","altText": "ようこそ！","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(msg_from,messages=container_obj)
        return

    if msg_text == 'user_id':
        line_bot_api.reply_message(msg_from,TextSendMessage(text=user_id))
        return

    else:
        if user_id == set[user_id]['user_id'] and set[user_id]['n'] == 3:
            set[user_id]['n'] = 4
            set[user_id]['twitter'] = msg_text
            data = data1(set[user_id]['twitter'])
            flex = {"type": "flex","altText": "確認","contents":data}
            container_obj = FlexSendMessage.new_from_json_dict(flex)
            line_bot_api.reply_message(msg_from,messages=container_obj)
            return
        if user_id == set[user_id]['user_id'] and set[user_id]['n'] == 5:
            set[user_id]['n'] = 6
            set[user_id]['d_n'] = msg_text
            data = data3(set[user_id]['d_n'])
            flex = {"type": "flex","altText": "確認","contents":data}
            container_obj = FlexSendMessage.new_from_json_dict(flex)
            line_bot_api.reply_message(msg_from,messages=container_obj)
            return
        if user_id == set[user_id]['user_id'] and set[user_id]['n'] == 7:
            set[user_id]['n'] = 8
            set[user_id]['d_t'] = msg_text
            data = data7(set[user_id]['d_t'])
            flex = {"type": "flex","altText": "確認","contents":data}
            container_obj = FlexSendMessage.new_from_json_dict(flex)
            line_bot_api.reply_message(msg_from,messages=container_obj)
            return




if __name__ == "__main__":
#    app.run()
    port =  int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
