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
    "url": "https://cdn.pixabay.com/photo/2015/06/19/21/24/the-road-815297_1280.jpg",
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
        "text": "集まれ動画編集者森",
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
                "text": "入るにあたっての注意事項の説明",
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
          "label": "注意事項を聞く",
          "data": "注意事項",
          "displayText": "注意事項を教えて！"
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
        "text": "注意事項の説明",
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
                "text": "ツイッターのアカウント名で参加する。",
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
          "label": "ツイッターの登録",
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
                "text": "・集まれ動画編集の森では信頼を大切にしています。",
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
                "text": "・信頼関係をつくる為、Twitterの名前での参加がルールで決まっています。",
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
                "text": "・この後自己紹介用のテンプレートを配布するにあたって自分のTwitter情報を登録してもらいます。"
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
        "text": "を送信してもらいます",
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
                "text": "・この後自己紹介用のテンプレートを配布するにあたって自分の動画編集歴を登録してもらいます。"
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
                "text": "[動画編集歴 例2]",
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
        "text": "上の二つの例を参考に",
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
                "text": "・この後自己紹介用のテンプレートを配布するにあたって自分の目標を登録してもらいます。"
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
                "text": "まずは案件を獲得する！",
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
                "text": "[目標 例2]",
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
                "text": "まだない",
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
        "text": "さあ、入ろう！",
        "weight": "bold",
        "size": "xxl",
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


def text(user_id):
    data = '名前:自分の名前を入力\n自分のTwitter:{twitter}\n動画編集歴:{d_n}\nこれからの目標:{d_t}\nみんなへ一言:'.format(twitter=set[user_id][twitter],d_n=set[user_id][d_n],d_t=set[user_id][d_t])
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
        data = data2()
        flex = {"type": "flex","altText": "twitter登録","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

    if "ok3" in postback_msg and user_id == set[user_id]['user_id'] and set[user_id]['n'] == 8:
        set[user_id]['n'] = 9
        text = text(user_id)
        line_bot_api.multicast(['U76d18383a9b659b9ab3d0e43d06c1e78'],TextSendMessage(text='誰かが参加しようとしています！\n[詳細]\nTwitter:{twitter}\n動画編集歴:{d_n}\n目標:{d_t}'.format(twitter=set[user_id][twitter],d_n=set[user_id][d_n],d_t=set[user_id][d_t])))
        data = data5(text)
        flex = {"type": "flex","altText": "テンプレート配布","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

    if "受け取る" in postback_msg and user_id == set[user_id]['user_id'] and set[user_id]['n'] == 9:
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

    if msg_text == '集まれ動画編集の森に入る':
        data = syoukai()
        set[user_id] = {'user_id':user_id,'n':1,'twitter':'','d_n':'','d_t':''}
        flex = {"type": "flex","altText": "ようこそ！","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(msg_from,messages=container_obj)
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
            data = data3(set[user_id]['d_t'])
            flex = {"type": "flex","altText": "確認","contents":data}
            container_obj = FlexSendMessage.new_from_json_dict(flex)
            line_bot_api.reply_message(msg_from,messages=container_obj)
            return




if __name__ == "__main__":
#    app.run()
    port =  int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
