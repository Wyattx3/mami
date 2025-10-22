"""
Script to add mock characters for testing
"""
import asyncio
import sys
sys.path.insert(0, '/Users/apple/tele scy')

from database.db_manager import db_manager
from models.character import Character

MOCK_CHARACTERS = [
    {"name": "Aung Aung", "mbti": "ENTJ", "zodiac": "Leo", "description": "ဦးဆောင်မှုရှိပြီး ခေါင်းဆောင်စွမ်းရည်ကောင်းသူ"},
    {"name": "Kyaw Kyaw", "mbti": "ESTP", "zodiac": "Aries", "description": "သတ္တိရှိပြီး စွန့်စားရဲသူ"},
    {"name": "Zaw Zaw", "mbti": "INTJ", "zodiac": "Aquarius", "description": "ဉာဏ်ရည်မြင့်ပြီး အကြံပေးနိုင်သူ"},
    {"name": "Hla Hla", "mbti": "ESTJ", "zodiac": "Capricorn", "description": "စီးပွားရေးကောင်းပြီး စီမံခန့်ခွဲတတ်သူ"},
    {"name": "Mya Mya", "mbti": "ENFJ", "zodiac": "Libra", "description": "စာနာတတ်ပြီး လိမ္မာယဥ်ကျေးသူ"},
    {"name": "Thiha", "mbti": "ISTP", "zodiac": "Scorpio", "description": "လက်တွေ့ကျပြီး ပြဿနာဖြေရှင်းတတ်သူ"},
    {"name": "Su Su", "mbti": "INFJ", "zodiac": "Pisces", "description": "နက်နဲစွာစဉ်းစားပြီး စာနာတတ်သူ"},
    {"name": "Ko Ko", "mbti": "ENTP", "zodiac": "Gemini", "description": "ဖန်တီးမှုရှိပြီး စိတ်ကူးစွမ်းရည်ကောင်းသူ"},
    {"name": "Nwe Nwe", "mbti": "ISTJ", "zodiac": "Virgo", "description": "တာဝန်သိပြီး စနစ်တကျလုပ်သူ"},
    {"name": "Win Win", "mbti": "ESFJ", "zodiac": "Cancer", "description": "ပူပင်တတ်ပြီး အများကိုဂရုစိုက်သူ"},
    {"name": "Phyu Phyu", "mbti": "INFP", "zodiac": "Taurus", "description": "စိတ်ကူးယဉ်တတ်ပြီး အနုပညာစိတ်ရှိသူ"},
    {"name": "Min Min", "mbti": "ESFP", "zodiac": "Sagittarius", "description": "ပျော်ရွှင်တတ်ပြီး စွန့်စားလိုသူ"}
]

async def add_mock_characters():
    """Add mock characters to database"""
    await db_manager.init_database()
    
    print("🎭 Adding mock characters...")
    for char_data in MOCK_CHARACTERS:
        character = Character(
            id=None,
            name=char_data["name"],
            mbti=char_data["mbti"],
            zodiac=char_data["zodiac"],
            description=char_data["description"]
        )
        
        try:
            char_id = await db_manager.add_character(character)
            print(f"✅ Added: {character.name} (ID: {char_id})")
        except Exception as e:
            print(f"❌ Error adding {character.name}: {e}")
    
    # Check total
    count = await db_manager.get_character_count()
    print(f"\n✅ Total characters in database: {count}")

if __name__ == "__main__":
    asyncio.run(add_mock_characters())

