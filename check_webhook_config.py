"""
Check webhook configuration status
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("WEBHOOK CONFIGURATION CHECK")
print("=" * 60)

webhook_url = os.getenv('WEBHOOK_URL')
webhook_path = os.getenv('WEBHOOK_PATH', '/webhook')
port = os.getenv('PORT', '8080')

print(f"\n1. WEBHOOK_URL: {repr(webhook_url)}")
print(f"   - Type: {type(webhook_url)}")
print(f"   - Length: {len(webhook_url) if webhook_url else 0}")
print(f"   - Bool value: {bool(webhook_url)}")

print(f"\n2. WEBHOOK_PATH: {repr(webhook_path)}")
print(f"3. PORT: {repr(port)}")

print(f"\n4. USE_WEBHOOK would be: {bool(webhook_url)}")

if webhook_url:
    print(f"\n✅ Webhook URL is set!")
    print(f"   Full webhook: {webhook_url}{webhook_path}")
else:
    print(f"\n❌ Webhook URL is NOT set!")
    print(f"   Bot will use POLLING mode")

print("\n" + "=" * 60)
print("EXPECTED ENVIRONMENT VARIABLES FOR WEBHOOK MODE:")
print("=" * 60)
print("""
WEBHOOK_URL=https://f639d579-2b5d-4427-993b-840b25023a71-prod.e1-us-east-azure.choreoapis.dev
WEBHOOK_PATH=/webhook
PORT=8080
""")

