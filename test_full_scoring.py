#!/usr/bin/env python3
"""
Comprehensive Test for Full Scoring Tables
Tests all 135 roles across 29 themes
"""
import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import logging
from data.themes import THEMES, get_theme_count
from data.full_scores import MBTI_SCORES, ZODIAC_SCORES
from services.scoring_service import scoring_service
from models.character import Character

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class TestResults:
    """Track test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_pass(self, test_name: str):
        self.passed += 1
        self.tests.append(("✅", test_name))
    
    def add_fail(self, test_name: str, error: str = ""):
        self.failed += 1
        self.tests.append(("❌", test_name, error))
        logger.error(f"❌ FAIL: {test_name} - {error}")
    
    def print_summary(self):
        print("\n" + "="*70)
        print("📊 TEST SUMMARY")
        print("="*70)
        
        for item in self.tests:
            if len(item) == 2:
                status, name = item
                print(f"{status} {name}")
            else:
                status, name, error = item
                print(f"{status} {name}")
                if error:
                    print(f"   → {error}")
        
        print("\n" + "="*70)
        total = self.passed + self.failed
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        if total > 0:
            print(f"Success Rate: {(self.passed/total*100):.1f}%")
        print("="*70)
        
        return self.failed == 0


def test_basic_structure(results: TestResults):
    """Test 1: Basic structure validation"""
    print("\n📊 Test 1: Scoring Tables Structure")
    print("-" * 70)
    
    # Count unique roles
    unique_roles = set()
    for theme in THEMES.values():
        for role_info in theme['roles'].values():
            unique_roles.add(role_info['name'])
    
    print(f"Unique roles in themes: {len(unique_roles)}")
    print(f"Roles in MBTI_SCORES: {len(MBTI_SCORES)}")
    print(f"Roles in ZODIAC_SCORES: {len(ZODIAC_SCORES)}")
    
    # Test MBTI_SCORES structure
    if len(MBTI_SCORES) >= 100:
        results.add_pass(f"MBTI scores table size: {len(MBTI_SCORES)} roles")
    else:
        results.add_fail("MBTI scores table", f"Only {len(MBTI_SCORES)} roles")
    
    # Test ZODIAC_SCORES structure
    if len(ZODIAC_SCORES) >= 100:
        results.add_pass(f"Zodiac scores table size: {len(ZODIAC_SCORES)} roles")
    else:
        results.add_fail("Zodiac scores table", f"Only {len(ZODIAC_SCORES)} roles")
    
    # Verify each role has all 16 MBTI types
    all_mbti = ['INTJ', 'INTP', 'ENTJ', 'ENTP', 'INFJ', 'INFP', 'ENFJ', 'ENFP',
                'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ', 'ISTP', 'ISFP', 'ESTP', 'ESFP']
    
    missing_mbti = []
    for role_name, scores in MBTI_SCORES.items():
        if len(scores) != 16:
            missing_mbti.append(role_name)
    
    if not missing_mbti:
        results.add_pass("All roles have 16 MBTI types")
    else:
        results.add_fail("MBTI completeness", f"{len(missing_mbti)} roles incomplete")
    
    # Verify each role has all 12 Zodiac signs
    all_zodiac = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    
    missing_zodiac = []
    for role_name, scores in ZODIAC_SCORES.items():
        if len(scores) != 12:
            missing_zodiac.append(role_name)
    
    if not missing_zodiac:
        results.add_pass("All roles have 12 Zodiac signs")
    else:
        results.add_fail("Zodiac completeness", f"{len(missing_zodiac)} roles incomplete")


def test_score_ranges(results: TestResults):
    """Test 2: Score range validation"""
    print("\n📊 Test 2: Score Range Validation (1-10)")
    print("-" * 70)
    
    invalid_mbti = []
    for role_name, scores in MBTI_SCORES.items():
        for mbti, score in scores.items():
            if not (1 <= score <= 10):
                invalid_mbti.append((role_name, mbti, score))
    
    if not invalid_mbti:
        results.add_pass("All MBTI scores in range 1-10")
    else:
        results.add_fail("MBTI score range", f"{len(invalid_mbti)} invalid scores")
    
    invalid_zodiac = []
    for role_name, scores in ZODIAC_SCORES.items():
        for zodiac, score in scores.items():
            if not (1 <= score <= 10):
                invalid_zodiac.append((role_name, zodiac, score))
    
    if not invalid_zodiac:
        results.add_pass("All Zodiac scores in range 1-10")
    else:
        results.add_fail("Zodiac score range", f"{len(invalid_zodiac)} invalid scores")


def test_kingdom_build_backward_compatibility(results: TestResults):
    """Test 3: Kingdom Build backward compatibility"""
    print("\n📊 Test 3: Kingdom Build Roles (Backward Compatibility)")
    print("-" * 70)
    
    kingdom_roles = ['ဘုရင်', 'စစ်သူကြီး', 'အကြံပေး', 'လယ်သမား', 'ဘုန်းကြီး']
    
    for role in kingdom_roles:
        if role in MBTI_SCORES and role in ZODIAC_SCORES:
            results.add_pass(f"Kingdom role: {role}")
        else:
            results.add_fail("Kingdom compatibility", f"Missing role: {role}")


def test_theme_specific_roles(results: TestResults):
    """Test 4: Theme-specific roles"""
    print("\n📊 Test 4: Theme-Specific Roles")
    print("-" * 70)
    
    # Test DC heroes
    dc_roles = ['Superman', 'Batman', 'Flash', 'Wonder Woman', 'Aquaman']
    for role in dc_roles:
        if role in MBTI_SCORES:
            results.add_pass(f"DC hero: {role}")
        else:
            results.add_fail("DC heroes", f"Missing: {role}")
    
    # Test Football players
    football_roles = ['Lionel Messi', 'Cristiano Ronaldo', 'Kylian Mbappe']
    for role in football_roles:
        if role in MBTI_SCORES:
            results.add_pass(f"Football: {role}")
        else:
            results.add_fail("Football players", f"Missing: {role}")
    
    # Test Myanmar singers
    singer_roles = ['လွှမ်းပိုင်', 'Bobby Soxer', 'Sai Sai Kham Leng']
    for role in singer_roles:
        if role in MBTI_SCORES:
            results.add_pass(f"Singer: {role}")
        else:
            results.add_fail("Myanmar singers", f"Missing: {role}")
    
    # Test Family roles
    family_roles = ['အဖိုး', 'အဖွား', 'အဖေ', 'အမေ']
    for role in family_roles:
        if role in MBTI_SCORES:
            results.add_pass(f"Family: {role}")
        else:
            results.add_fail("Family roles", f"Missing: {role}")


def test_suitable_mbti_alignment(results: TestResults):
    """Test 5: Suitable MBTI alignment"""
    print("\n📊 Test 5: Suitable MBTI High Scores")
    print("-" * 70)
    
    # Sample test: Check if suitable_mbti types get high scores
    test_cases = [
        ('Superman', ['ENTJ', 'ENFJ']),
        ('Batman', ['INTJ', 'ISTJ']),
        ('Messi', ['ISTP', 'ISFP']),
        ('အဖိုး', ['ISTJ', 'INTJ']),
    ]
    
    for role_name, suitable_types in test_cases:
        if role_name not in MBTI_SCORES:
            continue
        
        scores = MBTI_SCORES[role_name]
        high_scores = [mbti for mbti, score in scores.items() if score >= 8]
        
        # Check if at least one suitable type has high score
        has_high_score = any(mbti in high_scores for mbti in suitable_types)
        
        if has_high_score:
            results.add_pass(f"{role_name} suitable MBTI alignment")
        else:
            results.add_fail(f"{role_name} suitable MBTI", "No high scores for suitable types")


def test_scoring_calculation(results: TestResults):
    """Test 6: Actual scoring calculation"""
    print("\n📊 Test 6: Scoring Calculation")
    print("-" * 70)
    
    test_chars = [
        # High score examples
        Character(1, "Test Leader", "ENTJ", "Leo", ""),
        Character(2, "Test Warrior", "ESTP", "Aries", ""),
        Character(3, "Test Advisor", "INTJ", "Virgo", ""),
        # Low score examples
        Character(4, "Test Mismatch", "INFP", "Pisces", ""),
    ]
    
    test_roles = ['ဘုရင်', 'Superman', 'Messi', 'အဖိုး']
    
    passed = 0
    total = 0
    
    for char in test_chars[:1]:  # Test with first character
        for role in test_roles:
            if role not in MBTI_SCORES:
                continue
            
            total += 1
            score, explanation = scoring_service.calculate_character_score(char, role)
            
            if 1 <= score <= 10 and len(explanation) > 0:
                passed += 1
    
    if passed == total:
        results.add_pass(f"Scoring calculation: {passed}/{total}")
    else:
        results.add_fail("Scoring calculation", f"Only {passed}/{total} passed")


def test_all_themes(results: TestResults):
    """Test 7: All themes coverage"""
    print("\n📊 Test 7: All 29 Themes Coverage")
    print("-" * 70)
    
    covered_roles = 0
    total_roles = 0
    
    for theme_id, theme in THEMES.items():
        theme_covered = 0
        for round_num, role_info in theme['roles'].items():
            total_roles += 1
            role_name = role_info['name']
            
            if role_name in MBTI_SCORES and role_name in ZODIAC_SCORES:
                theme_covered += 1
                covered_roles += 1
        
        if theme_covered == 5:
            results.add_pass(f"Theme {theme_id}: {theme['name']}")
        else:
            results.add_fail(f"Theme {theme_id}", f"Only {theme_covered}/5 roles covered")
    
    print(f"\nTotal coverage: {covered_roles}/{total_roles} roles")


async def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 FULL SCORING TABLES TEST SUITE")
    print("Testing 135 roles across 29 themes")
    print("="*70)
    
    results = TestResults()
    
    test_basic_structure(results)
    test_score_ranges(results)
    test_kingdom_build_backward_compatibility(results)
    test_theme_specific_roles(results)
    test_suitable_mbti_alignment(results)
    test_scoring_calculation(results)
    test_all_themes(results)
    
    # Print summary
    success = results.print_summary()
    
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)

