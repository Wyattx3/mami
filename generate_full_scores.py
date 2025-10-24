#!/usr/bin/env python3
"""
Generate Full Scoring Tables for All 145 Roles
Uses suitable_mbti hints from themes.py to intelligently assign scores
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from data.themes import THEMES
from typing import Dict, List, Set


# All MBTI types
ALL_MBTI = [
    'INTJ', 'INTP', 'ENTJ', 'ENTP',
    'INFJ', 'INFP', 'ENFJ', 'ENFP',
    'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ',
    'ISTP', 'ISFP', 'ESTP', 'ESFP'
]

# All Zodiac signs
ALL_ZODIAC = [
    'Aries', 'Taurus', 'Gemini', 'Cancer',
    'Leo', 'Virgo', 'Libra', 'Scorpio',
    'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

# MBTI opposites (for low scoring)
MBTI_OPPOSITES = {
    'INTJ': ['ESFP', 'ESTP'],
    'INTP': ['ESFJ', 'ESTJ'],
    'ENTJ': ['ISFP', 'INFP'],
    'ENTP': ['ISFJ', 'ISTJ'],
    'INFJ': ['ESTP', 'ESFP'],
    'INFP': ['ESTJ', 'ENTJ'],
    'ENFJ': ['ISTP', 'ISTJ'],
    'ENFP': ['ISTJ', 'INTJ'],
    'ISTJ': ['ENFP', 'ENTP'],
    'ISFJ': ['ENTP', 'ENTJ'],
    'ESTJ': ['INFP', 'INTP'],
    'ESFJ': ['INTP', 'INTJ'],
    'ISTP': ['ENFJ', 'ESFJ'],
    'ISFP': ['ENTJ', 'ESTJ'],
    'ESTP': ['INFJ', 'INTJ'],
    'ESFP': ['INTJ', 'INTP']
}

# Role archetype to Zodiac mapping
ARCHETYPE_ZODIAC = {
    'leader': ['Leo', 'Aries', 'Capricorn', 'Scorpio'],
    'warrior': ['Aries', 'Scorpio', 'Leo', 'Sagittarius'],
    'advisor': ['Virgo', 'Aquarius', 'Capricorn', 'Scorpio'],
    'caring': ['Cancer', 'Pisces', 'Libra', 'Taurus'],
    'creative': ['Pisces', 'Aquarius', 'Gemini', 'Sagittarius'],
    'business': ['Capricorn', 'Taurus', 'Virgo', 'Scorpio'],
    'diplomatic': ['Libra', 'Pisces', 'Cancer', 'Taurus'],
    'family': ['Cancer', 'Taurus', 'Virgo', 'Capricorn'],
    'friendship': ['Gemini', 'Libra', 'Aquarius', 'Sagittarius'],
    'athletic': ['Aries', 'Leo', 'Sagittarius', 'Scorpio'],
    'artistic': ['Pisces', 'Cancer', 'Libra', 'Taurus']
}


def categorize_role(role_name: str, description: str, suitable_mbti: List[str]) -> str:
    """Determine role archetype based on name and description"""
    name_lower = role_name.lower()
    desc_lower = description.lower()
    
    # Leadership keywords
    if any(k in name_lower for k in ['king', 'queen', 'leader', 'captain', 'ဘုရင', 'သူကြီး', 'ဦးဆောင']):
        return 'leader'
    
    # Warrior keywords
    if any(k in name_lower for k in ['warrior', 'soldier', 'fighter', 'စစ်', 'တိုက']):
        return 'warrior'
    
    # Advisor/Wise keywords
    if any(k in name_lower for k in ['advisor', 'wise', 'counselor', 'အကြံ', 'ပညာ', 'ဉာဏ်']):
        return 'advisor'
    
    # Caring/Family keywords
    if any(k in name_lower for k in ['mother', 'father', 'grandpa', 'grandma', 'အမေ', 'အဖေ', 'အဖွား', 'အဖိုး', 'မိသားစု']):
        return 'caring'
    
    # Business keywords
    if any(k in name_lower for k in ['farmer', 'business', 'merchant', 'လယ်', 'စီးပွား', 'ကုန်သွယ်']):
        return 'business'
    
    # Diplomatic keywords
    if any(k in name_lower for k in ['monk', 'priest', 'diplomat', 'ဘုန်း', 'ယဉ်ကျေး']):
        return 'diplomatic'
    
    # Athletic/Sports keywords
    if any(k in name_lower for k in ['messi', 'ronaldo', 'player', 'footballer', 'athlete']):
        return 'athletic'
    
    # Artistic/Creative keywords
    if any(k in name_lower for k in ['singer', 'artist', 'creative', 'သီချင်း', 'အနုပညာ']):
        return 'artistic'
    
    # Check suitable_mbti patterns for hints
    extroverts = sum(1 for m in suitable_mbti if m.startswith('E'))
    thinking = sum(1 for m in suitable_mbti if 'T' in m)
    
    if extroverts >= 3:
        return 'friendship'
    elif thinking >= 3:
        return 'advisor'
    else:
        return 'family'


def generate_mbti_scores(role_name: str, suitable_mbti: List[str]) -> Dict[str, int]:
    """Generate MBTI scores for a role"""
    scores = {}
    
    # High scores for suitable types
    for mbti in suitable_mbti[:4]:  # Top 4 suitable
        if len(suitable_mbti) >= 4:
            idx = suitable_mbti.index(mbti)
            if idx == 0:
                scores[mbti] = 10
            elif idx == 1:
                scores[mbti] = 9
            elif idx == 2:
                scores[mbti] = 8
            else:
                scores[mbti] = 8
        else:
            scores[mbti] = 9
    
    # Get opposites of suitable types
    opposite_types = set()
    for mbti in suitable_mbti:
        opposite_types.update(MBTI_OPPOSITES.get(mbti, []))
    
    # Assign scores to remaining types
    for mbti in ALL_MBTI:
        if mbti in scores:
            continue
        
        if mbti in opposite_types:
            # Low score for opposite types
            scores[mbti] = 2
        elif mbti in suitable_mbti:
            # Medium-high for other suitable types
            scores[mbti] = 7
        else:
            # Check similarity (same letters)
            similarity = 0
            for suitable in suitable_mbti[:2]:  # Check top 2
                similarity += sum(a == b for a, b in zip(mbti, suitable))
            
            if similarity >= 2:
                scores[mbti] = 6
            elif similarity == 1:
                scores[mbti] = 4
            else:
                scores[mbti] = 3
    
    return scores


def generate_zodiac_scores(role_name: str, description: str, suitable_mbti: List[str]) -> Dict[str, int]:
    """Generate Zodiac scores for a role"""
    archetype = categorize_role(role_name, description, suitable_mbti)
    high_zodiac = ARCHETYPE_ZODIAC.get(archetype, ['Leo', 'Aries', 'Capricorn', 'Scorpio'])
    
    scores = {}
    
    # High scores for archetype-matching zodiacs
    for i, zodiac in enumerate(high_zodiac):
        if i == 0:
            scores[zodiac] = 10
        elif i == 1:
            scores[zodiac] = 9
        elif i == 2:
            scores[zodiac] = 8
        else:
            scores[zodiac] = 7
    
    # Medium scores for remaining
    remaining = [z for z in ALL_ZODIAC if z not in high_zodiac]
    for i, zodiac in enumerate(remaining):
        if i < len(remaining) // 2:
            scores[zodiac] = 5
        elif i < len(remaining) * 3 // 4:
            scores[zodiac] = 4
        else:
            scores[zodiac] = 2
    
    return scores


def extract_all_roles() -> Dict[str, Dict]:
    """Extract all unique roles from themes"""
    roles_data = {}
    
    for theme_id, theme in THEMES.items():
        for round_num, role_info in theme['roles'].items():
            role_name = role_info['name']
            if role_name not in roles_data:
                roles_data[role_name] = {
                    'name': role_name,
                    'description': role_info['description'],
                    'suitable_mbti': role_info['suitable_mbti'],
                    'themes': []
                }
            roles_data[role_name]['themes'].append(theme['name'])
    
    return roles_data


def generate_all_scores():
    """Generate complete scoring tables"""
    roles_data = extract_all_roles()
    
    print('"""')
    print('Full Scoring Tables for All 145 Roles')
    print('Generated automatically from themes.py')
    print('"""')
    print()
    print('# MBTI Scores (1-10) for each role')
    print('MBTI_SCORES = {')
    
    for role_name, role_info in sorted(roles_data.items()):
        mbti_scores = generate_mbti_scores(role_name, role_info['suitable_mbti'])
        print(f"    '{role_name}': {{")
        
        # Print in groups of 4 for readability
        items = list(mbti_scores.items())
        for i in range(0, len(items), 4):
            group = items[i:i+4]
            line = ', '.join(f"'{mbti}': {score}" for mbti, score in group)
            if i + 4 < len(items):
                print(f"        {line},")
            else:
                print(f"        {line}")
        
        print('    },')
    
    print('}')
    print()
    print('# Zodiac Scores (1-10) for each role')
    print('ZODIAC_SCORES = {')
    
    for role_name, role_info in sorted(roles_data.items()):
        zodiac_scores = generate_zodiac_scores(
            role_name, 
            role_info['description'], 
            role_info['suitable_mbti']
        )
        print(f"    '{role_name}': {{")
        
        # Print in groups of 4 for readability
        items = list(zodiac_scores.items())
        for i in range(0, len(items), 4):
            group = items[i:i+4]
            line = ', '.join(f"'{zodiac}': {score}" for zodiac, score in group)
            if i + 4 < len(items):
                print(f"        {line},")
            else:
                print(f"        {line}")
        
        print('    },')
    
    print('}')
    print()
    print(f'# Total roles: {len(roles_data)}')
    print(f'# MBTI entries: {len(roles_data) * 16}')
    print(f'# Zodiac entries: {len(roles_data) * 12}')
    print(f'# Total score entries: {len(roles_data) * 28}')


if __name__ == '__main__':
    generate_all_scores()

