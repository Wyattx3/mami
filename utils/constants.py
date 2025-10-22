"""
Game constants and enums
"""

# Game Roles (5 rounds)
ROLES = {
    1: {
        'name': 'ဘုရင်',
        'description': 'ဦးဆောင်နိုင်တဲ့သူ',
        'suitable_mbti': ['ENTJ', 'ENFJ', 'ESTJ', 'ENTP']
    },
    2: {
        'name': 'စစ်သူကြီး',
        'description': 'သတ္တိရှိသူ',
        'suitable_mbti': ['ESTP', 'ISTP', 'ESTJ', 'ISTJ']
    },
    3: {
        'name': 'အကြံပေး',
        'description': 'ဉာဏ်ပညာရှိသူ',
        'suitable_mbti': ['INTJ', 'INTP', 'INFJ', 'ENTP']
    },
    4: {
        'name': 'လယ်သမား',
        'description': 'စီးပွားရှာတတ်သူ',
        'suitable_mbti': ['ISTJ', 'ISFJ', 'ESTJ', 'ESFJ']
    },
    5: {
        'name': 'ဘုန်းကြီး',
        'description': 'လိမ္မာယဥ်ကျေးသူ',
        'suitable_mbti': ['INFJ', 'INFP', 'ENFJ', 'ISFJ']
    }
}

# MBTI Types
MBTI_TYPES = [
    'INTJ', 'INTP', 'ENTJ', 'ENTP',
    'INFJ', 'INFP', 'ENFJ', 'ENFP',
    'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ',
    'ISTP', 'ISFP', 'ESTP', 'ESFP'
]

# Zodiac Signs
ZODIAC_SIGNS = [
    'Aries', 'Taurus', 'Gemini', 'Cancer',
    'Leo', 'Virgo', 'Libra', 'Scorpio',
    'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

# Game Status
GAME_STATUS = {
    'LOBBY': 'lobby',
    'IN_PROGRESS': 'in_progress',
    'FINISHED': 'finished',
    'CANCELLED': 'cancelled'
}

# Callback Data Patterns
CALLBACK_PATTERNS = {
    'JOIN_LOBBY': 'join_lobby',
    'QUIT_LOBBY': 'quit_lobby',
    'VOTE': 'vote_{game_id}_{round}_{team}_{character_id}',
    'DETAILS': 'details_{game_id}_{team}_{role}'
}


