"""
Game Themes with Random Selection
30+ different themes for variety and replayability
"""
import random
from typing import Dict, Any, List


# All available themes
THEMES = {
    # Kingdom Build Series
    1: {
        'id': 1,
        'name': 'Kingdom Build',
        'emoji': '👑',
        'category': 'kingdom',
        'roles': {
            1: {'name': 'ဘုရင်', 'description': 'ဦးဆောင်နိုင်တဲ့သူ', 'suitable_mbti': ['ENTJ', 'ENFJ', 'ESTJ', 'ENTP']},
            2: {'name': 'စစ်သူကြီး', 'description': 'သတ္တိရှိသူ', 'suitable_mbti': ['ESTP', 'ISTP', 'ESTJ', 'ISTJ']},
            3: {'name': 'အကြံပေး', 'description': 'ဉာဏ်ပညာရှိသူ', 'suitable_mbti': ['INTJ', 'INTP', 'INFJ', 'ENTP', 'ESTJ']},
            4: {'name': 'လယ်သမား', 'description': 'စီးပွားရှာတတ်သူ', 'suitable_mbti': ['ISTJ', 'ISFJ', 'ESTJ', 'ESFJ']},
            5: {'name': 'ဘုန်းကြီး', 'description': 'လိမ္မာယဥ်ကျေးသူ', 'suitable_mbti': ['INFJ', 'INFP', 'ENFJ', 'ISFJ']}
        }
    },
    2: {
        'id': 2,
        'name': 'Kingdom Build 2',
        'emoji': '👑',
        'category': 'kingdom',
        'roles': {
            1: {'name': 'ဘုရင်', 'description': 'ဦးဆောင်မင်းသား', 'suitable_mbti': ['ENTJ', 'ENFJ', 'ESTJ', 'ENTP']},
            2: {'name': 'ဘုရင်မ', 'description': 'ဂုဏ်သိက္ခာရှိသူ', 'suitable_mbti': ['ENFJ', 'ESFJ', 'INFJ', 'ISFJ']},
            3: {'name': 'အိမ်ရှေ့စံ', 'description': 'တာဝန်ယူတတ်သူ', 'suitable_mbti': ['ESTJ', 'ISTJ', 'ENTJ', 'INTJ']},
            4: {'name': 'မင်းသမီး', 'description': 'လှပသော်လည်း ဉာဏ်ရှိသူ', 'suitable_mbti': ['ENFP', 'INFP', 'ENFJ', 'INFJ']},
            5: {'name': 'ပြည့်တန်ဆာ', 'description': 'အပြုသဘောဆောင်သူ', 'suitable_mbti': ['ESFJ', 'ISFJ', 'ENFJ', 'INFJ']}
        }
    },
    3: {
        'id': 3,
        'name': 'Kingdom Build 3',
        'emoji': '👑',
        'category': 'kingdom',
        'roles': {
            1: {'name': 'စစ်သူကြီး', 'description': 'သတ္တိနှင့် ရဲစွမ်းသူ', 'suitable_mbti': ['ESTP', 'ISTP', 'ESTJ', 'ISTJ']},
            2: {'name': 'အမတ်', 'description': 'တရားမျှတသူ', 'suitable_mbti': ['INTJ', 'ENTJ', 'ISTJ', 'ESTJ']},
            3: {'name': 'အကြံပေး', 'description': 'ပညာရှိဉာဏ်ရှိသူ', 'suitable_mbti': ['INTJ', 'INTP', 'INFJ', 'ENTP', 'ESTJ']},
            4: {'name': 'မိန်းမစိုး', 'description': 'လုပ်ငန်းစွမ်းဆောင်ရည်ရှိသူ', 'suitable_mbti': ['ENTJ', 'ESTJ', 'ENFJ', 'ESFJ']},
            5: {'name': 'စားတော်ချက်', 'description': 'ဖန်တီးမှုရှိသူ', 'suitable_mbti': ['ISFP', 'ESFP', 'INFP', 'ENFP']}
        }
    },
    4: {
        'id': 4,
        'name': 'Kingdom Build 4',
        'emoji': '👑',
        'category': 'kingdom',
        'roles': {
            1: {'name': 'ဘုန်းကြီး', 'description': 'စိတ်ဓာတ်မြင့်မားသူ', 'suitable_mbti': ['INFJ', 'INFP', 'ENFJ', 'ISFJ']},
            2: {'name': 'မြင်းထိန်း', 'description': 'တာဝန်သိတတ်သူ', 'suitable_mbti': ['ISTP', 'ISTJ', 'ESTP', 'ESTJ']},
            3: {'name': 'သူတောင်းစား', 'description': 'နှိမ့်ချသော်လည်း ပြည့်စုံသူ', 'suitable_mbti': ['INFP', 'ISFP', 'INTP', 'ISTP']},
            4: {'name': 'သချိုင်းစောင့်', 'description': 'တည်ငြိမ်ပြီး တာဝန်သိသူ', 'suitable_mbti': ['ISTJ', 'ISFJ', 'INTJ', 'INFJ']},
            5: {'name': 'လယ်သမား', 'description': 'အလုပ်ကြိုးစားသူ', 'suitable_mbti': ['ISTJ', 'ISFJ', 'ESTJ', 'ESFJ']}
        }
    },
    5: {
        'id': 5,
        'name': 'Kingdom Build 5',
        'emoji': '👑',
        'category': 'kingdom',
        'roles': {
            1: {'name': 'သစ္စာဖောက်', 'description': 'လိမ္မာပါးနပ်သူ', 'suitable_mbti': ['ENTP', 'ESTP', 'ENTJ', 'ESTJ']},
            2: {'name': 'သူလျှို', 'description': 'သတင်းစုံစမ်းတတ်သူ', 'suitable_mbti': ['INTP', 'INTJ', 'ISTP', 'ISTJ']},
            3: {'name': 'လူယုံ', 'description': 'တည်ကြည်ယုံကြည်သူ', 'suitable_mbti': ['ISFJ', 'ESFJ', 'INFJ', 'ENFJ']},
            4: {'name': 'သူဌေးကြီး', 'description': 'စီးပွားရေးကျွမ်းကျင်သူ', 'suitable_mbti': ['ENTJ', 'ESTJ', 'INTJ', 'ISTJ']},
            5: {'name': 'သတင်းစူးစမ်းရေး', 'description': 'အမှန်တရားရှာဖွေသူ', 'suitable_mbti': ['ENTP', 'INTP', 'ENFP', 'INFP']}
        }
    },
    6: {
        'id': 6,
        'name': 'Kingdom Build 6',
        'emoji': '👑',
        'category': 'kingdom',
        'roles': {
            1: {'name': 'ဘဏ္ဍာရေးဝန်ကြီး', 'description': 'ငွေကြေးစီမံခန့်ခွဲသူ', 'suitable_mbti': ['INTJ', 'ENTJ', 'ISTJ', 'ESTJ']},
            2: {'name': 'ဥပဒေအရာရှိ', 'description': 'တရားမျှတမှုရှာသူ', 'suitable_mbti': ['INTJ', 'ISTJ', 'ENTJ', 'ESTJ']},
            3: {'name': 'ပြည့်သူအကျိုးစီမံ', 'description': 'လူမှုကူညီတတ်သူ', 'suitable_mbti': ['ENFJ', 'ESFJ', 'INFJ', 'ISFJ']},
            4: {'name': 'အခွန်ကောက်အမတ်', 'description': 'စည်းကမ်းတင်းကျပ်သူ', 'suitable_mbti': ['ESTJ', 'ISTJ', 'ENTJ', 'INTJ']},
            5: {'name': 'ကုန်သွယ်သမား', 'description': 'စွန့်ဦးတီထွင်သူ', 'suitable_mbti': ['ESTP', 'ENTP', 'ESTJ', 'ENTJ']}
        }
    },
    
    # Family Build Series
    7: {
        'id': 7,
        'name': 'Family Build',
        'emoji': '👨‍👩‍👧‍👦',
        'category': 'family',
        'roles': {
            1: {'name': 'အဖိုး', 'description': 'အတွေ့အကြုံများပြီး ဉာဏ်ပညာရှိသူ', 'suitable_mbti': ['ISTJ', 'INTJ', 'ESTJ', 'ENTJ']},
            2: {'name': 'အဖွား', 'description': 'ချစ်ခင်တောင့်တသူ', 'suitable_mbti': ['ISFJ', 'ESFJ', 'INFJ', 'ENFJ']},
            3: {'name': 'အဖေ', 'description': 'မိသားစုကို ကာကွယ်စောင့်ရှောက်သူ', 'suitable_mbti': ['ISTJ', 'ESTJ', 'ISTP', 'ESTP']},
            4: {'name': 'အမေ', 'description': 'ချစ်ခင်ဂရုစိုက်သူ', 'suitable_mbti': ['ISFJ', 'ESFJ', 'INFJ', 'ENFJ']},
            5: {'name': 'ပထွေး', 'description': 'ဝန်ထုပ်ဝန်ပိုးထမ်းဆောင်သူ', 'suitable_mbti': ['ISTJ', 'ISFJ', 'ESTJ', 'ESFJ']}
        }
    },
    8: {
        'id': 8,
        'name': 'Family Build 2',
        'emoji': '👨‍👩‍👧‍👦',
        'category': 'family',
        'roles': {
            1: {'name': 'သား', 'description': 'တာဝန်ယူနိုင်သော မျိုးဆက်သစ်', 'suitable_mbti': ['ENTJ', 'ESTJ', 'ENTP', 'ESTP']},
            2: {'name': 'သမီး', 'description': 'နူးညံ့သိမ်မွေ့ပြီး ဉာဏ်ရှိသူ', 'suitable_mbti': ['INFJ', 'ENFJ', 'ISFJ', 'ESFJ']},
            3: {'name': 'မြေး', 'description': 'ကစားတတ်သော နောက်မျိုးဆက်', 'suitable_mbti': ['ENFP', 'ESFP', 'INFP', 'ISFP']},
            4: {'name': 'ဦးလေး', 'description': 'ဗဟုသုတများသူ', 'suitable_mbti': ['INTP', 'ENTP', 'INTJ', 'ENTJ']},
            5: {'name': 'အဒေါ်', 'description': 'သတင်းပြန်တတ်သော ဆွေမျိုး', 'suitable_mbti': ['ESFJ', 'ENFJ', 'ESFP', 'ENFP']}
        }
    },
    9: {
        'id': 9,
        'name': 'Family Build 3',
        'emoji': '👨‍👩‍👧‍👦',
        'category': 'family',
        'roles': {
            1: {'name': 'ယောင်းမ', 'description': 'မိသားစုသစ်ဝင်ရောက်သူ', 'suitable_mbti': ['ISFJ', 'ESFJ', 'INFJ', 'ENFJ']},
            2: {'name': 'သားမက်', 'description': 'တာဝန်ထမ်းဆောင်သူ', 'suitable_mbti': ['ISTJ', 'ESTJ', 'ISTP', 'ESTP']},
            3: {'name': 'ချွေးမ', 'description': 'ဝင်ရောက်နေထိုင်သူ', 'suitable_mbti': ['ISFJ', 'ESFJ', 'INFJ', 'ENFJ']},
            4: {'name': 'သားမက်', 'description': 'မိသားစုအတွက် ကြိုးစားသူ', 'suitable_mbti': ['ISTJ', 'ESTJ', 'ISTP', 'ESTP']},
            5: {'name': 'မိထွေး', 'description': 'မိသားစုအသစ်ဦးဆောင်သူ', 'suitable_mbti': ['ESTJ', 'ENTJ', 'ESFJ', 'ENFJ']}
        }
    },
    10: {
        'id': 10,
        'name': 'Family Build 4',
        'emoji': '👨‍👩‍👧‍👦',
        'category': 'family',
        'roles': {
            1: {'name': 'ယောက်ခမ္မ', 'description': 'ကူညီပေးတတ်သူ', 'suitable_mbti': ['ESFJ', 'ENFJ', 'ISFJ', 'INFJ']},
            2: {'name': 'ယောက်ခထီး', 'description': 'အတူတကွနေထိုင်သူ', 'suitable_mbti': ['ESTP', 'ESFP', 'ENTP', 'ENFP']},
            3: {'name': 'ဦးလေး', 'description': 'ဗဟုသုတများသူ', 'suitable_mbti': ['INTP', 'ENTP', 'INTJ', 'ENTJ']},
            4: {'name': 'အဒေါ်', 'description': 'ဂရုစိုက်တတ်သူ', 'suitable_mbti': ['ESFJ', 'ENFJ', 'ISFJ', 'INFJ']},
            5: {'name': 'ကလေး', 'description': 'ပျော်ရွှင်စိတ်ကူးကြွသူ', 'suitable_mbti': ['ENFP', 'ESFP', 'INFP', 'ISFP']}
        }
    },
    
    # Friend Build Series
    11: {
        'id': 11,
        'name': 'Friend Build',
        'emoji': '🤝',
        'category': 'friendship',
        'roles': {
            1: {'name': 'ဦးဆောင်တက်သူ', 'description': 'အုပ်စုကို ဦးဆောင်နိုင်သူ', 'suitable_mbti': ['ENTJ', 'ENFJ', 'ESTJ', 'ENTP']},
            2: {'name': 'တက်ကြွသူ', 'description': 'စွမ်းအင်ပြည့်ဝသူ', 'suitable_mbti': ['ESTP', 'ESFP', 'ENTP', 'ENFP']},
            3: {'name': 'ဖာခေါင်း', 'description': 'ရယ်မောပျော်ရွှင်စေသူ', 'suitable_mbti': ['ENTP', 'ENFP', 'ESTP', 'ESFP']},
            4: {'name': 'နတ်သမီး', 'description': 'လှပရုပ်ရည်ရှိသူ', 'suitable_mbti': ['ENFJ', 'ESFJ', 'INFJ', 'ISFJ']},
            5: {'name': 'ငြင်းလေ့ရှိသူ', 'description': 'စိတ်ထားခိုင်မာသူ', 'suitable_mbti': ['INTJ', 'INTP', 'ENTJ', 'ENTP']}
        }
    },
    12: {
        'id': 12,
        'name': 'Friend Build 2',
        'emoji': '🤝',
        'category': 'friendship',
        'roles': {
            1: {'name': 'ကြာကူလီ', 'description': 'အလုပ်ကြိုးစားသူ', 'suitable_mbti': ['ISTJ', 'ISFJ', 'ESTJ', 'ESFJ']},
            2: {'name': 'အေးဆေးနေတက်သူ', 'description': 'တည်ငြိမ်ပြီး စိတ်အေးသူ', 'suitable_mbti': ['ISTP', 'ISFP', 'INTP', 'INFP']},
            3: {'name': 'ညာဏ်ကောင်းသူ', 'description': 'ဉာဏ်ရှိတက်သူ', 'suitable_mbti': ['INTJ', 'INTP', 'ENTJ', 'ENTP']},
            4: {'name': 'စာတော်သူ', 'description': 'ပညာတတ်သူ', 'suitable_mbti': ['INTJ', 'INTP', 'INFJ', 'INFP']},
            5: {'name': 'ဖော်ဖော်ရွေရွေရှိသူ', 'description': 'ပွင့်လင်းသော စိတ်ထားရှိသူ', 'suitable_mbti': ['ENFP', 'ESFP', 'ENFJ', 'ESFJ']}
        }
    },
    13: {
        'id': 13,
        'name': 'Friend Build 3',
        'emoji': '🤝',
        'category': 'friendship',
        'roles': {
            1: {'name': 'ခင်မို့မို့အေး', 'description': 'ထူးခြားသော အထောက်အထားရှိသူ', 'suitable_mbti': ['ENFP', 'INFP', 'ENFJ', 'INFJ']},
            2: {'name': 'ပန်းနုသွေး', 'description': 'နူးညံ့သိမ်မွေ့သူ', 'suitable_mbti': ['ISFP', 'INFP', 'ISFJ', 'INFJ']},
            3: {'name': 'ပျော်ပျော်နေသူ', 'description': 'အမြဲပျော်ရွှင်နေသူ', 'suitable_mbti': ['ENFP', 'ESFP', 'ENTP', 'ESTP']},
            4: {'name': 'တည်ကြည်သူ', 'description': 'ယုံကြည်ရသော သူငယ်ချင်း', 'suitable_mbti': ['ISFJ', 'ISTJ', 'INFJ', 'INTJ']},
            5: {'name': 'ရယ်အောင်လုပ်ပေးတက်သူ', 'description': 'ဟာသဉာဏ်ရှိသူ', 'suitable_mbti': ['ENTP', 'ENFP', 'ESTP', 'ESFP']}
        }
    },
    14: {
        'id': 14,
        'name': 'Friend Build 4',
        'emoji': '🤝',
        'category': 'friendship',
        'roles': {
            1: {'name': 'ခွေးဝဲစား', 'description': 'အခွင့်ကောင်းယူတတ်သူ', 'suitable_mbti': ['ESTP', 'ENTP', 'ESFP', 'ENFP']},
            2: {'name': 'သူတောင်းစား', 'description': 'အမြဲတောင်းတတ်သူ', 'suitable_mbti': ['ESFP', 'ENFP', 'ESTP', 'ENTP']},
            3: {'name': 'အမြဲနောက်ကျသူ', 'description': 'အချိန်မဟန်သူ', 'suitable_mbti': ['INFP', 'INTP', 'ISFP', 'ISTP']},
            4: {'name': 'စာမလုပ်သူ', 'description': 'ပညာမစိုက်ထုတ်သူ', 'suitable_mbti': ['ESTP', 'ESFP', 'ISTP', 'ISFP']},
            5: {'name': 'စကားများသူ', 'description': 'အမြဲပြောတတ်သူ', 'suitable_mbti': ['ENFP', 'ESFP', 'ENTP', 'ESTP']}
        }
    },
    15: {
        'id': 15,
        'name': 'Friend Build 5',
        'emoji': '🤝',
        'category': 'friendship',
        'roles': {
            1: {'name': 'ကျားဖြန့် (လူလိမ်)', 'description': 'လိမ်လည်တတ်သူ', 'suitable_mbti': ['ENTP', 'ESTP', 'ENTJ', 'ESTJ']},
            2: {'name': 'အကုသိုလ်', 'description': 'မကောင်းမှုပြုလုပ်သူ', 'suitable_mbti': ['ESTP', 'ENTP', 'ISTP', 'INTP']},
            3: {'name': 'ဆော့လေ့ရှိသူ (heart player)', 'description': 'အချစ်ရေးကစားသူ', 'suitable_mbti': ['ESTP', 'ESFP', 'ENTP', 'ENFP']},
            4: {'name': 'အပြင်သွားလေ့ရှိသူ', 'description': 'အပြင်ထွက်ကြိုက်သူ', 'suitable_mbti': ['ESTP', 'ESFP', 'ENTP', 'ENFP']},
            5: {'name': 'နှာဘူး', 'description': 'မာန်မာနရှိသူ', 'suitable_mbti': ['ENTJ', 'ESTJ', 'INTJ', 'ISTJ']}
        }
    },
    
    # Relationship Build Series
    16: {
        'id': 16,
        'name': 'Relationship Build',
        'emoji': '💕',
        'category': 'relationship',
        'roles': {
            1: {'name': 'ဒုတိယလူ', 'description': 'လျှို့ဝှက်အချစ်ရေး', 'suitable_mbti': ['ESTP', 'ENTP', 'ESFP', 'ENFP']},
            2: {'name': 'သစ္စာရှိသူ', 'description': 'တစ်သက်သာတည်ကြည်သူ', 'suitable_mbti': ['ISFJ', 'ISTJ', 'INFJ', 'INTJ']},
            3: {'name': 'ဖောက်ပြန်သူ', 'description': 'သစ္စာမရှိသူ', 'suitable_mbti': ['ESTP', 'ENTP', 'ESFP', 'ENFP']},
            4: {'name': 'ဖောက်ပြန်ခံရသူ', 'description': 'နာကျင်မှုခံစားရသူ', 'suitable_mbti': ['INFP', 'ISFP', 'INFJ', 'ISFJ']},
            5: {'name': 'သဝန်တိုတက်သူ', 'description': 'မနာလိုတတ်သူ', 'suitable_mbti': ['ESFJ', 'ENFJ', 'ISFJ', 'INFJ']}
        }
    },
    17: {
        'id': 17,
        'name': 'Relationship Build 2',
        'emoji': '💕',
        'category': 'relationship',
        'roles': {
            1: {'name': 'အရမ်းချစ်တက်သူ', 'description': 'အချစ်ကို အရာရာထက် တန်ဖိုးထားသူ', 'suitable_mbti': ['ENFP', 'INFP', 'ENFJ', 'INFJ']},
            2: {'name': 'လိမ်တက်တဲ့သူ', 'description': 'မမှန်မကန် ပြောတတ်သူ', 'suitable_mbti': ['ENTP', 'ESTP', 'ENTJ', 'ESTJ']},
            3: {'name': 'ညှိနှိုင်းတဲ့သူ', 'description': 'ပြဿနာဖြေရှင်းတတ်သူ', 'suitable_mbti': ['ENFJ', 'ESFJ', 'INFJ', 'ISFJ']},
            4: {'name': 'အားပေးလေ့ရှိသူ', 'description': 'မွေ့ရာပေးတတ်သူ', 'suitable_mbti': ['ENFJ', 'ESFJ', 'INFJ', 'ISFJ']},
            5: {'name': 'တည်ကြည်သူ', 'description': 'ယုံကြည်ရသူ', 'suitable_mbti': ['ISTJ', 'ISFJ', 'INTJ', 'INFJ']}
        }
    },
    18: {
        'id': 18,
        'name': 'Relationship Build 3',
        'emoji': '💕',
        'category': 'relationship',
        'roles': {
            1: {'name': 'Red Flag', 'description': 'အန္တရာယ်ရှိသော ချစ်သူ', 'suitable_mbti': ['ESTP', 'ENTP', 'ESTJ', 'ENTJ']},
            2: {'name': 'Green Flag', 'description': 'ကောင်းမွန်သော ချစ်သူ', 'suitable_mbti': ['ISFJ', 'ESFJ', 'INFJ', 'ENFJ']},
            3: {'name': 'Ex Lover', 'description': 'အတိတ်က အချစ်ရေး', 'suitable_mbti': ['INFP', 'ENFP', 'ISFP', 'ESFP']},
            4: {'name': 'မရွေး (ရွေးချယ်မခံရသူ)', 'description': 'အမြဲကျန်ခဲ့ရသူ', 'suitable_mbti': ['INFP', 'ISFP', 'INTP', 'ISTP']},
            5: {'name': 'အေးတိအေးစက် (Cold Heart)', 'description': 'စိတ်ခံစားမှု မပြသူ', 'suitable_mbti': ['INTJ', 'ISTJ', 'INTP', 'ISTP']}
        }
    },
    
    # DC Build Series
    19: {
        'id': 19,
        'name': 'DC Build',
        'emoji': '🦸',
        'category': 'superhero',
        'roles': {
            1: {'name': 'Superman', 'description': 'အစွမ်းထက်ဆုံး သူရဲကောင်း', 'suitable_mbti': ['ENFJ', 'ESFJ', 'ENTJ', 'ESTJ']},
            2: {'name': 'Batman', 'description': 'ဉာဏ်ရှိ လှံ့ဩဗဟာ', 'suitable_mbti': ['INTJ', 'ISTJ', 'ENTJ', 'ESTJ']},
            3: {'name': 'Flash', 'description': 'အမြန်ဆုံး သူရဲကောင်း', 'suitable_mbti': ['ENFP', 'ESFP', 'ENTP', 'ESTP']},
            4: {'name': 'Wonder Woman', 'description': 'ခွန်အားကြီး အမျိုးသမီး သူရဲကောင်း', 'suitable_mbti': ['ENFJ', 'ESFJ', 'ENTJ', 'ESTJ']},
            5: {'name': 'Aquaman', 'description': 'ပင်လယ်ရေအောက် ဘုရင်', 'suitable_mbti': ['ISTP', 'ESTP', 'ISTJ', 'ESTJ']}
        }
    },
    20: {
        'id': 20,
        'name': 'DC Build 2',
        'emoji': '🦸',
        'category': 'superhero',
        'roles': {
            1: {'name': 'Green Lantern', 'description': 'စိတ်ကူးစိတ်သန်းရှိသူ', 'suitable_mbti': ['ENFP', 'INFP', 'ENTP', 'INTP']},
            2: {'name': 'Cyborg', 'description': 'နည်းပညာကျွမ်းကျင်သူ', 'suitable_mbti': ['INTJ', 'INTP', 'ISTJ', 'ISTP']},
            3: {'name': 'Martian Manhunter', 'description': 'စိတ်ဖတ်နိုင်သူ', 'suitable_mbti': ['INFJ', 'INTJ', 'ENFJ', 'ENTJ']},
            4: {'name': 'Green Arrow', 'description': 'လေးစွမ်းကျွမ်းကျင်သူ', 'suitable_mbti': ['ISTP', 'ESTP', 'ISTJ', 'ESTJ']},
            5: {'name': 'Black Canary', 'description': 'အသံစွမ်းအား ပိုင်ရှင်', 'suitable_mbti': ['ESFP', 'ENFP', 'ESTP', 'ENTP']}
        }
    },
    
    # Marvel Build Series
    21: {
        'id': 21,
        'name': 'Marvel Build',
        'emoji': '🦸',
        'category': 'superhero',
        'roles': {
            1: {'name': 'Spider-Man', 'description': 'လျင်မြန်သော သူရဲကောင်းငယ်', 'suitable_mbti': ['ENFP', 'INFP', 'ENTP', 'INTP']},
            2: {'name': 'Iron Man', 'description': 'ပါရမီရှင် တီထွင်သူ', 'suitable_mbti': ['ENTP', 'ENTJ', 'INTP', 'INTJ']},
            3: {'name': 'Captain America', 'description': 'ခေါင်းဆောင် သူရဲကောင်း', 'suitable_mbti': ['ISTJ', 'ESTJ', 'ISFJ', 'ESFJ']},
            4: {'name': 'Thor', 'description': 'မိုးကြိုးထီးဘုရား', 'suitable_mbti': ['ESTP', 'ESFP', 'ENTP', 'ENFP']},
            5: {'name': 'Hulk', 'description': 'ခွန်အားထက်သန်သူ', 'suitable_mbti': ['ISTP', 'ESTP', 'ISTJ', 'ESTJ']}
        }
    },
    22: {
        'id': 22,
        'name': 'Marvel Build 2',
        'emoji': '🦸',
        'category': 'superhero',
        'roles': {
            1: {'name': 'Black Widow', 'description': 'လိမ္မာပါးနပ်သော သူလျှို', 'suitable_mbti': ['ISTP', 'ESTP', 'INTJ', 'ENTJ']},
            2: {'name': 'Hawkeye', 'description': 'လေးသမား ကျွမ်းကျင်သူ', 'suitable_mbti': ['ISTP', 'ISTJ', 'ESTP', 'ESTJ']},
            3: {'name': 'Doctor Strange', 'description': 'မန္တန်လုပ်ဆောင်နိုင်သူ', 'suitable_mbti': ['INTJ', 'INTP', 'ENTJ', 'ENTP']},
            4: {'name': 'Scarlet Witch', 'description': 'စွမ်းအားထက်သန်သူ', 'suitable_mbti': ['INFP', 'INFJ', 'ENFP', 'ENFJ']},
            5: {'name': 'Vision', 'description': 'ဉာဏ်ရည်ထက်မြက်သော AI', 'suitable_mbti': ['INTJ', 'INTP', 'INFJ', 'INFP']}
        }
    },
    
    # Football Player Build Series
    23: {
        'id': 23,
        'name': 'Football Player Build',
        'emoji': '⚽',
        'category': 'sports',
        'roles': {
            1: {'name': 'Lionel Messi', 'description': 'ဘောလုံးမှုန်ဆရာကြီး', 'suitable_mbti': ['INFP', 'ISFP', 'INTP', 'ISTP']},
            2: {'name': 'Cristiano Ronaldo', 'description': 'မာန်မာနကြီး ကစားသမား', 'suitable_mbti': ['ENTJ', 'ESTJ', 'ENTP', 'ESTP']},
            3: {'name': 'Kylian Mbappe', 'description': 'အမြန်ဆုံး ကစားသမား', 'suitable_mbti': ['ESTP', 'ESFP', 'ENTP', 'ENFP']},
            4: {'name': 'Erling Haaland', 'description': 'ဂိုးသွင်းစက်ရုပ်', 'suitable_mbti': ['ISTP', 'ISTJ', 'ESTP', 'ESTJ']},
            5: {'name': 'Lamine Yamal', 'description': 'ငယ်ရွယ်သော အစွမ်းထက်သူ', 'suitable_mbti': ['ENFP', 'ESFP', 'ENTP', 'ESTP']}
        }
    },
    24: {
        'id': 24,
        'name': 'Football Player Build 2',
        'emoji': '⚽',
        'category': 'sports',
        'roles': {
            1: {'name': 'Neymar', 'description': 'စွမ်းရည်များသော ကစားသမား', 'suitable_mbti': ['ESFP', 'ENFP', 'ESTP', 'ENTP']},
            2: {'name': 'Jude Bellingham', 'description': 'ချစ်စရာကောင်းသော ငယ်သား', 'suitable_mbti': ['ENFP', 'ESFP', 'ENTJ', 'ESTJ']},
            3: {'name': 'Mary Earps', 'description': 'အကောင်းဆုံး ဂိုးသမား', 'suitable_mbti': ['ISTJ', 'ESTJ', 'ISTP', 'ESTP']},
            4: {'name': 'David Beckham', 'description': 'ကန့်ကွက်သူဆရာကြီး', 'suitable_mbti': ['ISFJ', 'ESFJ', 'ISTJ', 'ESTJ']},
            5: {'name': 'Harry Kane', 'description': 'ဂိုးသွင်းကျွမ်းကျင်သူ', 'suitable_mbti': ['ISTJ', 'ESTJ', 'ISFJ', 'ESFJ']}
        }
    },
    25: {
        'id': 25,
        'name': 'Football Player Build 3',
        'emoji': '⚽',
        'category': 'sports',
        'roles': {
            1: {'name': 'Mohamed Salah', 'description': 'အီဂျစ်မှ ဘုရင်', 'suitable_mbti': ['ISFP', 'ISTP', 'ESFP', 'ESTP']},
            2: {'name': 'Declan Rice', 'description': 'အလယ်တန်းကြီး', 'suitable_mbti': ['ISTJ', 'ESTJ', 'ISFJ', 'ESFJ']},
            3: {'name': 'Phil Foden', 'description': 'ငယ်ရွယ်သော ပါရမီရှင်', 'suitable_mbti': ['ENFP', 'INFP', 'ENTP', 'INTP']},
            4: {'name': 'Diogo Dalot', 'description': 'ခံစစ်သည်ကြီး', 'suitable_mbti': ['ISTP', 'ISTJ', 'ESTP', 'ESTJ']},
            5: {'name': 'Harry Maguire', 'description': 'ခေါင်းဆောင် ခံစစ်သည်', 'suitable_mbti': ['ISTJ', 'ESTJ', 'ISFJ', 'ESFJ']}
        }
    },
    
    # Myanmar Singers Build Series
    26: {
        'id': 26,
        'name': 'Myanmar Singers Build',
        'emoji': '🎤',
        'category': 'music',
        'roles': {
            1: {'name': 'လွှမ်းပိုင်', 'description': 'ရော့ဂျယ်သီချင်းဆရာ', 'suitable_mbti': ['ENFP', 'ENTP', 'ESFP', 'ESTP']},
            2: {'name': 'Bobby Soxer', 'description': 'ခေတ်အဆန္ဒ ပေါ်ပ်သီဆိုသူ', 'suitable_mbti': ['ESFP', 'ENFP', 'ESTP', 'ENTP']},
            3: {'name': 'Sai Sai Kham Leng', 'description': 'အချစ်သီချင်း ဘုရင်', 'suitable_mbti': ['INFP', 'ISFP', 'ENFP', 'ESFP']},
            4: {'name': 'Yung Hugo', 'description': 'ရေပ်သီချင်း အနုပညာရှင်', 'suitable_mbti': ['ENTP', 'ENFP', 'ESTP', 'ESFP']},
            5: {'name': 'Shwe Htoo', 'description': 'ရိုးရာသီချင်း ဆရာကြီး', 'suitable_mbti': ['INFJ', 'INFP', 'ISFJ', 'ISFP']}
        }
    },
    27: {
        'id': 27,
        'name': 'Myanmar Singers Build 2',
        'emoji': '🎤',
        'category': 'music',
        'roles': {
            1: {'name': 'Htoo Eain Thin', 'description': 'ရော့ကန် အနုပညာရှင်', 'suitable_mbti': ['ENFP', 'ESFP', 'ENTP', 'ESTP']},
            2: {'name': 'Zaw Paing', 'description': 'ပေါ့ပ်သီချင်း ဆရာ', 'suitable_mbti': ['ENFP', 'ESFP', 'INFP', 'ISFP']},
            3: {'name': 'Lay Phyu', 'description': 'ခံစားမှုရှိသော သီဆိုသူ', 'suitable_mbti': ['INFP', 'ISFP', 'INFJ', 'ISFJ']},
            4: {'name': 'Raymond', 'description': 'ကောင်းမွန်သော အသံပိုင်ရှင်', 'suitable_mbti': ['ENFP', 'ESFP', 'INFP', 'ISFP']},
            5: {'name': 'Khin Maung Toe', 'description': 'ရိုးရာအချစ် သီဆိုသူ', 'suitable_mbti': ['ISFJ', 'ISTJ', 'INFJ', 'INTJ']}
        }
    },
    28: {
        'id': 28,
        'name': 'Myanmar Singers Build 3',
        'emoji': '🎤',
        'category': 'music',
        'roles': {
            1: {'name': 'Chan Chan', 'description': 'ရေပ် အနုပညာရှင်', 'suitable_mbti': ['ENTP', 'ESTP', 'ENFP', 'ESFP']},
            2: {'name': 'Thin Zar Maw', 'description': 'အမျိုးသမီး သီဆိုသူကြီး', 'suitable_mbti': ['ESFJ', 'ENFJ', 'ESFP', 'ENFP']},
            3: {'name': 'G Fatt', 'description': 'ရေပ်ဂီတ လူငယ်', 'suitable_mbti': ['ENTP', 'ESTP', 'ENFP', 'ESFP']},
            4: {'name': 'Yair Yint Aung', 'description': 'ပေါ့ပ် အနုပညာရှင်', 'suitable_mbti': ['ENFP', 'ESFP', 'ENTP', 'ESTP']},
            5: {'name': 'Lil Kee Boi', 'description': 'ရေပ်သီချင်း လူငယ်ကြီး', 'suitable_mbti': ['ESTP', 'ENTP', 'ESFP', 'ENFP']}
        }
    },
    29: {
        'id': 29,
        'name': 'Myanmar Singers Build 4',
        'emoji': '🎤',
        'category': 'music',
        'roles': {
            1: {'name': 'Shine', 'description': 'ရော့ဂျယ် အနုပညာရှင်', 'suitable_mbti': ['ENFP', 'ENTP', 'ESFP', 'ESTP']},
            2: {'name': 'Wine Su Khaing Thein', 'description': 'နူးညံ့သော အသံပိုင်ရှင်', 'suitable_mbti': ['ISFP', 'INFP', 'ISFJ', 'INFJ']},
            3: {'name': 'Phyu Phyu Kyaw Thein', 'description': 'အချစ်သီချင်း အနုပညာရှင်', 'suitable_mbti': ['ESFJ', 'ENFJ', 'ISFJ', 'INFJ']},
            4: {'name': 'R Zarni', 'description': 'ခေတ်သစ် သီဆိုသူ', 'suitable_mbti': ['ENFP', 'ESFP', 'ENTP', 'ESTP']},
            5: {'name': 'Kyar Pauk', 'description': 'ထူးခြားသော အသံလှိုင်း', 'suitable_mbti': ['INFP', 'ISFP', 'ENFP', 'ESFP']}
        }
    },
    
    # Supernatural Series
    30: {
        'id': 30,
        'name': 'နာနာဘာဝ Build',
        'emoji': '👻',
        'category': 'supernatural',
        'roles': {
            1: {'name': 'သရဲ', 'description': 'ကြောက်မက်ဖွယ် ဝိညာဥ်', 'suitable_mbti': ['INFP', 'INFJ', 'INTP', 'INTJ']},
            2: {'name': 'တစ္ဆေ', 'description': 'စိတ်ဆိုးလွန်းသော နတ်', 'suitable_mbti': ['ESTP', 'ENTP', 'ESTJ', 'ENTJ']},
            3: {'name': 'ပြိတ္တာ', 'description': 'ဆာလောင်နေသော ဝိညာဥ်', 'suitable_mbti': ['ISFP', 'INFP', 'ISTP', 'INTP']},
            4: {'name': 'အသူရကယ်', 'description': 'အစွမ်းထက် နတ်ဆိုး', 'suitable_mbti': ['ENTJ', 'ESTJ', 'ENTP', 'ESTP']},
            5: {'name': 'ဝိညာဥ်', 'description': 'သဘာဝလွန် စွမ်းအား', 'suitable_mbti': ['INFJ', 'INTJ', 'ENFJ', 'ENTJ']}
        }
    },
    31: {
        'id': 31,
        'name': 'နာနာဘာဝ Build 2',
        'emoji': '👻',
        'category': 'supernatural',
        'roles': {
            1: {'name': 'နတ်ဆိုး', 'description': 'ဆိုးညစ်သော နတ်သား', 'suitable_mbti': ['ENTJ', 'ESTJ', 'ENTP', 'INTJ']},
            2: {'name': 'ဥစ္စာစောင့်', 'description': 'ဘဏ္ဍာစောင့်ရှောက်သူ', 'suitable_mbti': ['ISTJ', 'ESTJ', 'INTJ', 'ENTJ']},
            3: {'name': 'ရုပ်က္ခစိုး', 'description': 'ရုပ်ဝတ္ထုလောက အစိုးရ', 'suitable_mbti': ['ENTJ', 'ESTJ', 'INTJ', 'ISTJ']},
            4: {'name': 'ချီးစားစုန်း', 'description': 'အနာဂတ်မြင်နိုင်သူ', 'suitable_mbti': ['INFJ', 'INTJ', 'ENFJ', 'ENTJ']},
            5: {'name': 'သဘက်', 'description': 'သဘာဝတရား နတ်', 'suitable_mbti': ['INFP', 'ISFP', 'ENFP', 'ESFP']}
        }
    },
    
    # Occupation Series
    32: {
        'id': 32,
        'name': 'အလုပ်အကိုင် Build',
        'emoji': '💼',
        'category': 'occupation',
        'roles': {
            1: {'name': 'နွားကျောင်းသား', 'description': 'တိရစ္ဆာန်ထိန်းသူ', 'suitable_mbti': ['ISFJ', 'ISTJ', 'ESFJ', 'ESTJ']},
            2: {'name': 'အိမ်သာသန့်ရှင်းရေး', 'description': 'သန့်ရှင်းရေးအလုပ်သမား', 'suitable_mbti': ['ISFJ', 'ISTJ', 'ISFP', 'ISTP']},
            3: {'name': 'ခြံစောင့်', 'description': 'လုံခြုံရေးတာဝန်ခံ', 'suitable_mbti': ['ISTJ', 'ISTP', 'ESTJ', 'ESTP']},
            4: {'name': 'ပလုံကောက်သမား', 'description': 'လယ်ယာအလုပ်သမား', 'suitable_mbti': ['ISFJ', 'ISTJ', 'ESFJ', 'ESTJ']},
            5: {'name': 'အပြာသရုပ်ဆောင်', 'description': 'ရဲရင့်သော အနုပညာရှင်', 'suitable_mbti': ['ESFP', 'ESTP', 'ENFP', 'ENTP']}
        }
    },
    33: {
        'id': 33,
        'name': 'အလုပ်အကိုင် Build 2',
        'emoji': '💼',
        'category': 'occupation',
        'roles': {
            1: {'name': 'စားပွဲထိုး', 'description': 'ဧည့်ဝန်ဆောင်မှုပေးသူ', 'suitable_mbti': ['ESFJ', 'ENFJ', 'ESFP', 'ENFP']},
            2: {'name': 'ချဲဒိုင်', 'description': 'ဆောက်လုပ်ရေးအလုပ်သမား', 'suitable_mbti': ['ISTP', 'ESTP', 'ISTJ', 'ESTJ']},
            3: {'name': 'တပ်မတော်သားကြီး', 'description': 'စစ်ဘက်ခေါင်းဆောင်', 'suitable_mbti': ['ESTJ', 'ENTJ', 'ISTJ', 'INTJ']},
            4: {'name': 'ဟက်ကာ', 'description': 'နည်းပညာကျွမ်းကျင်သူ', 'suitable_mbti': ['INTP', 'INTJ', 'ISTP', 'ENTP']},
            5: {'name': 'သူတောင်းစား', 'description': 'နှိမ့်ချသော ဘဝ', 'suitable_mbti': ['INFP', 'ISFP', 'INTP', 'ISTP']}
        }
    },
    
    # Body Features Series
    34: {
        'id': 34,
        'name': 'ခန္ဓာကိုယ် Build',
        'emoji': '🧍',
        'category': 'physical',
        'roles': {
            1: {'name': 'ဖင်ကြီးသူ', 'description': 'ထင်ရှားသော ခန္ဓာလက္ခဏာ', 'suitable_mbti': ['ESFP', 'ESTP', 'ENFP', 'ENTP']},
            2: {'name': 'အသားမဲသူ', 'description': 'သဘာဝအသားအရောင်', 'suitable_mbti': ['ISFP', 'ISTP', 'ESFP', 'ESTP']},
            3: {'name': 'ဖက်တီး', 'description': 'ကျန်းမာသော ခန္ဓာကိုယ်', 'suitable_mbti': ['ESFJ', 'ISFJ', 'ESFP', 'ISFP']},
            4: {'name': 'သွားခေါ', 'description': 'ထူးခြားသော အပြုံး', 'suitable_mbti': ['ENFP', 'ESFP', 'INFP', 'ISFP']},
            5: {'name': 'မျက်ပြူး', 'description': 'မျက်လုံးသေးသူ', 'suitable_mbti': ['INFP', 'ISFP', 'INTP', 'ISTP']}
        }
    },
    35: {
        'id': 35,
        'name': 'ခန္ဓာကိုယ် Build 2',
        'emoji': '🧍',
        'category': 'physical',
        'roles': {
            1: {'name': 'ဂျပု', 'description': 'အရပ်ပိတ်သူ', 'suitable_mbti': ['INFP', 'ISFP', 'INTP', 'ISTP']},
            2: {'name': 'ဝါးခြမ်းပြား', 'description': 'ပိန်ပိန်လှလှ', 'suitable_mbti': ['INFP', 'ISFP', 'INTP', 'ISTP']},
            3: {'name': 'ကတုံး', 'description': 'အရပ်တိုသူ', 'suitable_mbti': ['ISFP', 'ISTP', 'ESFP', 'ESTP']},
            4: {'name': 'ခပ်ချောချော', 'description': 'လှပသော အသွင်အပြင်', 'suitable_mbti': ['ESFP', 'ENFP', 'ISFP', 'INFP']},
            5: {'name': 'ကျပ်မပြည့်', 'description': 'ပိန်ပိန်ကိုယ်', 'suitable_mbti': ['INTP', 'INFP', 'ISTP', 'ISFP']}
        }
    },
    
    # Behavior Series
    36: {
        'id': 36,
        'name': 'အမူအကျင့် Build',
        'emoji': '🎭',
        'category': 'behavior',
        'roles': {
            1: {'name': 'တက်ကြွသူ', 'description': 'စွမ်းအင်ပြည့်ဝသူ', 'suitable_mbti': ['ESTP', 'ESFP', 'ENTP', 'ENFP']},
            2: {'name': 'ငပျင်း', 'description': 'လှုပ်ရှားမှုနည်းသူ', 'suitable_mbti': ['INTP', 'INFP', 'ISTP', 'ISFP']},
            3: {'name': 'လူလိမ်', 'description': 'လိမ်ညာတတ်သူ', 'suitable_mbti': ['ENTP', 'ESTP', 'ENTJ', 'ESTJ']},
            4: {'name': 'အချိန်မတိကျသူ', 'description': 'အချိန်ပျက်တတ်သူ', 'suitable_mbti': ['ENFP', 'INFP', 'ENTP', 'INTP']},
            5: {'name': 'ကတိဖျက်သူ', 'description': 'ကတိမတည်သူ', 'suitable_mbti': ['ESTP', 'ESFP', 'ENTP', 'ENFP']}
        }
    },
    37: {
        'id': 37,
        'name': 'အမူအကျင့် Build 2',
        'emoji': '🎭',
        'category': 'behavior',
        'roles': {
            1: {'name': 'တကိုယ်ကောင်းဆန်သူ', 'description': 'ကိုယ်ကျိုးစီးပွားသမား', 'suitable_mbti': ['ENTJ', 'ESTJ', 'INTJ', 'ISTJ']},
            2: {'name': 'မာနကြီးသူ', 'description': 'မာန်မာနရှိသူ', 'suitable_mbti': ['ENTJ', 'ESTJ', 'ENTP', 'ESTP']},
            3: {'name': 'နွားဆန်သူ', 'description': 'စိတ်မပြောင်းလဲသူ', 'suitable_mbti': ['ISTJ', 'ESTJ', 'INTJ', 'ISTP']},
            4: {'name': 'အပျော်မက်သူ', 'description': 'ပျော်ရွှင်မှုကြိုက်သူ', 'suitable_mbti': ['ESFP', 'ENFP', 'ESTP', 'ENTP']},
            5: {'name': 'ပိုက်ဆံချေးသူ', 'description': 'စီးပွားရေးကျွမ်းကျင်သူ', 'suitable_mbti': ['ENTJ', 'ESTJ', 'INTJ', 'ISTJ']}
        }
    },
    
    # UC Build Series
    38: {
        'id': 38,
        'name': 'UC Build',
        'emoji': '👥',
        'category': 'group',
        'roles': {
            1: {'name': 'ဉာဏ်ကောင်းသူ', 'description': 'ထက်မြက်သော စိတ်ဉာဏ်', 'suitable_mbti': ['INTJ', 'INTP', 'ENTJ', 'ENTP', 'ESTJ']},
            2: {'name': 'စကားများသူ', 'description': 'စကားပြောတတ်သူ', 'suitable_mbti': ['ENFP', 'ESFP', 'ENTP', 'ESTP']},
            3: {'name': 'ဉာဏ်နည်းသူ', 'description': 'ရိုးရှင်းသော စိတ်', 'suitable_mbti': ['ISFP', 'ESFP', 'ISFJ', 'ESFJ']},
            4: {'name': 'စိတ်ကောက်လွယ်သူ', 'description': 'ထိခိုက်လွယ်သော စိတ်', 'suitable_mbti': ['INFP', 'ISFP', 'INFJ', 'ISFJ']},
            5: {'name': 'သဘောထားကြီးသူ', 'description': 'ရင့်ကျက်သော စိတ်ထား', 'suitable_mbti': ['ENFJ', 'INFJ', 'ENTJ', 'INTJ']}
        }
    }
}


def get_random_theme() -> Dict[str, Any]:
    """Get a random theme from all available themes
    
    Returns:
        Random theme dictionary
    """
    theme_ids = list(THEMES.keys())
    random_id = random.choice(theme_ids)
    return THEMES[random_id]


def get_theme_by_id(theme_id: int) -> Dict[str, Any]:
    """Get theme by ID
    
    Args:
        theme_id: Theme ID
        
    Returns:
        Theme dictionary or None if not found
    """
    return THEMES.get(theme_id)


def get_all_themes() -> Dict[int, Dict[str, Any]]:
    """Get all available themes
    
    Returns:
        Dictionary of all themes
    """
    return THEMES


def get_theme_count() -> int:
    """Get total number of themes
    
    Returns:
        Number of themes
    """
    return len(THEMES)


def get_themes_by_category(category: str) -> List[Dict[str, Any]]:
    """Get all themes in a specific category
    
    Args:
        category: Category name (kingdom, family, friendship, relationship, superhero, sports, music)
        
    Returns:
        List of themes in that category
    """
    return [theme for theme in THEMES.values() if theme['category'] == category]

