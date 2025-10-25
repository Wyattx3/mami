# Scoring Adjustment: ESTJ + Aquarius for Advisory Roles

## Date: 2025-10-25

## User Request
User requested that **ESTJ + Aquarius** combination should receive **perfect score (10)** for intelligent/advisory roles ("ဉာဏ်ကောင်းတဲ့နေရာတွေ အကြံပေးတဲ့နေရာတွေ").

## Rationale
- **ESTJ Personality:** 
  - Practical, organized, decisive
  - Natural leaders and managers
  - Fact-based decision makers
  - Strategic executors

- **Aquarius Zodiac:**
  - Innovative, intellectual, humanitarian
  - Original thinker, visionary
  - Independent, analytical

- **Combined Strengths:**
  - Strategic thinking with practical execution
  - Innovative ideas grounded in reality
  - Leadership with intellectual depth
  - Perfect for advisory/counselor roles

## Changes Made

### 1. Updated `data/full_scores.py`

**Role: အကြံပေး (Advisor/Counselor)**

**Before:**
```python
'အကြံပေး': {
    'INTJ': 10, 'INTP': 9, 'INFJ': 8, 'ENTP': 8,
    'ENTJ': 6, 'INFP': 6, 'ENFJ': 6, 'ENFP': 6,
    'ISTJ': 2, 'ISFJ': 2, 'ESTJ': 2, 'ESFJ': 2,  # ❌ ESTJ = 2
    'ISTP': 6, 'ISFP': 6, 'ESTP': 2, 'ESFP': 2
}
```

**After:**
```python
'အကြံပေး': {
    'INTJ': 10, 'INTP': 9, 'INFJ': 8, 'ENTP': 8,
    'ENTJ': 6, 'INFP': 6, 'ENFJ': 6, 'ENFP': 6,
    'ISTJ': 6, 'ISFJ': 2, 'ESTJ': 10, 'ESFJ': 2,  # ✅ ESTJ = 10
    'ISTP': 6, 'ISFP': 6, 'ESTP': 2, 'ESFP': 2
}
```

**Zodiac scores (updated):**
```python
'အကြံပေး': {
    'Aquarius': 10,  # ✅ Boosted from 9 → 10
    ...
}
```

### 2. Updated `data/themes.py`

Added **ESTJ** to `suitable_mbti` for both **အကြံပေး** roles:

**Theme 1 (Kingdom Build) - Role 3:**
```python
3: {'name': 'အကြံပေး', 'description': 'ဉာဏ်ပညာရှိသူ', 
    'suitable_mbti': ['INTJ', 'INTP', 'INFJ', 'ENTP', 'ESTJ']},  # Added ESTJ
```

**Theme 3 (Kingdom Build 3) - Role 3:**
```python
3: {'name': 'အကြံပေး', 'description': 'ပညာရှိဉာဏ်ရှိသူ', 
    'suitable_mbti': ['INTJ', 'INTP', 'INFJ', 'ENTP', 'ESTJ']},  # Added ESTJ
```

## Impact

### Score Comparison for ESTJ + Aquarius:

**Before:**
- MBTI: 2/10
- Zodiac: 9/10
- **Combined: 11 points (Average: 5.5/10)**

**After:**
- MBTI: 10/10 ✅
- Zodiac: 10/10 ✅
- **Combined: 20 points (Average: 10.0/10)** 🎯 PERFECT SCORE!

### Result:
- **ESTJ + Aquarius** characters will now excel in advisory/counselor roles
- Reflects the combination of practical leadership (ESTJ) with innovative thinking (Aquarius)
- Scoring now matches user's gameplay expectations

## Files Changed
1. `data/full_scores.py` - Updated MBTI score for အကြံပေး role
2. `data/themes.py` - Added ESTJ to suitable_mbti lists
3. `SCORING_ADJUSTMENT_ESTJ_AQUARIUS.md` - This documentation

## Testing
No code logic changes required. Scoring changes will take effect immediately in:
- Character-role matching calculations
- Round scoring evaluations
- Final game results

## Notes
- This is a game balance adjustment based on user feedback
- Other roles with similar advisory/strategic nature may need similar adjustments in the future
- Consider reviewing other ESTJ combinations for strategic roles

