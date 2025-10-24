"""
Test Message Delivery System
Verify reliable message delivery with retry logic
"""
import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent))

from utils.message_delivery import MessageDelivery
from telegram.error import TimedOut, NetworkError, RetryAfter, Forbidden


class TestResults:
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, test_name: str):
        self.total += 1
        self.passed += 1
        print(f"✅ PASS: {test_name}")
    
    def add_fail(self, test_name: str, reason: str):
        self.total += 1
        self.failed += 1
        self.errors.append((test_name, reason))
        print(f"❌ FAIL: {test_name}")
        print(f"   Reason: {reason}")
    
    def summary(self):
        print("\n" + "="*70)
        print("📊 TEST SUMMARY")
        print("="*70)
        print(f"Total Tests: {self.total}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"Success Rate: {(self.passed/self.total)*100:.1f}%")
        
        if self.errors:
            print("\n❌ Failed Tests:")
            for test_name, reason in self.errors:
                print(f"  - {test_name}: {reason}")
        
        print("="*70)


results = TestResults()


async def test_successful_delivery():
    """Test successful message delivery on first attempt"""
    print("\n✅ Test: Successful Delivery (First Attempt)")
    print("-" * 70)
    
    delivery = MessageDelivery()
    mock_bot = AsyncMock()
    mock_message = MagicMock()
    mock_message.message_id = 12345
    mock_bot.send_message = AsyncMock(return_value=mock_message)
    
    result = await delivery.send_message_with_retry(
        mock_bot,
        chat_id=123,
        text="Test message"
    )
    
    if result == mock_message:
        results.add_pass("Message delivered on first attempt")
    else:
        results.add_fail("First attempt", f"Expected message, got {result}")
    
    if mock_bot.send_message.call_count == 1:
        results.add_pass("Only one send attempt made")
    else:
        results.add_fail("Send count", f"Expected 1, got {mock_bot.send_message.call_count}")


async def test_retry_on_timeout():
    """Test retry logic on timeout"""
    print("\n🔄 Test: Retry on Timeout")
    print("-" * 70)
    
    delivery = MessageDelivery()
    mock_bot = AsyncMock()
    mock_message = MagicMock()
    
    # Fail twice, succeed on third
    mock_bot.send_message = AsyncMock(
        side_effect=[TimedOut("Timeout 1"), TimedOut("Timeout 2"), mock_message]
    )
    
    result = await delivery.send_message_with_retry(
        mock_bot,
        chat_id=123,
        text="Test message"
    )
    
    if result == mock_message:
        results.add_pass("Message delivered after retries")
    else:
        results.add_fail("Retry success", f"Expected message, got {result}")
    
    if mock_bot.send_message.call_count == 3:
        results.add_pass("Correct number of retries (3)")
    else:
        results.add_fail("Retry count", f"Expected 3, got {mock_bot.send_message.call_count}")


async def test_max_retries_exhausted():
    """Test when all retries are exhausted"""
    print("\n❌ Test: Max Retries Exhausted")
    print("-" * 70)
    
    delivery = MessageDelivery()
    mock_bot = AsyncMock()
    
    # Always timeout
    mock_bot.send_message = AsyncMock(
        side_effect=TimedOut("Always timeout")
    )
    
    result = await delivery.send_message_with_retry(
        mock_bot,
        chat_id=123,
        text="Test message"
    )
    
    if result is None:
        results.add_pass("Returns None after exhausting retries")
    else:
        results.add_fail("Exhausted retries", f"Expected None, got {result}")
    
    if mock_bot.send_message.call_count == 3:
        results.add_pass("Made 3 retry attempts")
    else:
        results.add_fail("Retry attempts", f"Expected 3, got {mock_bot.send_message.call_count}")
    
    # Check failed messages stored
    failed = delivery.get_failed_messages()
    if len(failed) == 1:
        results.add_pass("Failed message stored")
    else:
        results.add_fail("Failed storage", f"Expected 1, got {len(failed)}")


async def test_rate_limiting():
    """Test handling of rate limiting (RetryAfter)"""
    print("\n⏱️ Test: Rate Limiting (RetryAfter)")
    print("-" * 70)
    
    delivery = MessageDelivery()
    mock_bot = AsyncMock()
    mock_message = MagicMock()
    
    # Rate limited, then success
    mock_bot.send_message = AsyncMock(
        side_effect=[RetryAfter(2), mock_message]
    )
    
    result = await delivery.send_message_with_retry(
        mock_bot,
        chat_id=123,
        text="Test message"
    )
    
    if result == mock_message:
        results.add_pass("Message delivered after rate limit")
    else:
        results.add_fail("Rate limit handling", f"Expected message, got {result}")


async def test_forbidden_error():
    """Test handling of Forbidden error (user blocked bot)"""
    print("\n🚫 Test: Forbidden Error (User Blocked Bot)")
    print("-" * 70)
    
    delivery = MessageDelivery()
    mock_bot = AsyncMock()
    
    # User blocked bot
    mock_bot.send_message = AsyncMock(
        side_effect=Forbidden("Bot was blocked by the user")
    )
    
    result = await delivery.send_message_with_retry(
        mock_bot,
        chat_id=123,
        text="Test message"
    )
    
    if result is None:
        results.add_pass("Returns None for blocked user")
    else:
        results.add_fail("Forbidden handling", f"Expected None, got {result}")
    
    # Should not retry for Forbidden
    if mock_bot.send_message.call_count == 1:
        results.add_pass("No retry for Forbidden error")
    else:
        results.add_fail("Forbidden retry", f"Should not retry, but called {mock_bot.send_message.call_count} times")


async def test_network_error_retry():
    """Test retry on network error"""
    print("\n🌐 Test: Network Error Retry")
    print("-" * 70)
    
    delivery = MessageDelivery()
    mock_bot = AsyncMock()
    mock_message = MagicMock()
    
    # Network error, then success
    mock_bot.send_message = AsyncMock(
        side_effect=[NetworkError("Connection failed"), mock_message]
    )
    
    result = await delivery.send_message_with_retry(
        mock_bot,
        chat_id=123,
        text="Test message"
    )
    
    if result == mock_message:
        results.add_pass("Message delivered after network error")
    else:
        results.add_fail("Network error recovery", f"Expected message, got {result}")


async def test_bulk_sending():
    """Test bulk message sending"""
    print("\n📨 Test: Bulk Message Sending")
    print("-" * 70)
    
    delivery = MessageDelivery()
    mock_bot = AsyncMock()
    mock_message = MagicMock()
    mock_bot.send_message = AsyncMock(return_value=mock_message)
    
    recipients = [
        {'chat_id': 101, 'username': 'User1'},
        {'chat_id': 102, 'username': 'User2'},
        {'chat_id': 103, 'username': 'User3'},
    ]
    
    stats = await delivery.send_bulk_messages(
        mock_bot,
        recipients,
        "Hello {username}!",
        rate_limit_delay=0.01
    )
    
    if stats['sent'] == 3 and stats['failed'] == 0:
        results.add_pass("Bulk sending successful")
    else:
        results.add_fail("Bulk sending", f"Sent: {stats['sent']}, Failed: {stats['failed']}")
    
    if mock_bot.send_message.call_count == 3:
        results.add_pass("All bulk messages sent")
    else:
        results.add_fail("Bulk count", f"Expected 3, got {mock_bot.send_message.call_count}")


async def test_failed_message_tracking():
    """Test failed message tracking"""
    print("\n📝 Test: Failed Message Tracking")
    print("-" * 70)
    
    delivery = MessageDelivery()
    mock_bot = AsyncMock()
    mock_bot.send_message = AsyncMock(side_effect=TimedOut("Timeout"))
    
    # Send multiple messages that will fail
    await delivery.send_message_with_retry(mock_bot, 101, "Message 1")
    await delivery.send_message_with_retry(mock_bot, 102, "Message 2")
    
    failed = delivery.get_failed_messages()
    
    if len(failed) == 2:
        results.add_pass("Failed messages tracked")
    else:
        results.add_fail("Failed tracking", f"Expected 2, got {len(failed)}")
    
    # Clear failed messages
    delivery.clear_failed_messages()
    failed_after_clear = delivery.get_failed_messages()
    
    if len(failed_after_clear) == 0:
        results.add_pass("Failed messages cleared")
    else:
        results.add_fail("Clear failed", f"Expected 0, got {len(failed_after_clear)}")


async def main():
    """Run all message delivery tests"""
    print("="*70)
    print("📨 MESSAGE DELIVERY SYSTEM TEST SUITE")
    print("="*70)
    print("\nTesting reliable message delivery with retry logic...\n")
    
    try:
        # Run tests
        await test_successful_delivery()
        await test_retry_on_timeout()
        await test_max_retries_exhausted()
        await test_rate_limiting()
        await test_forbidden_error()
        await test_network_error_retry()
        await test_bulk_sending()
        await test_failed_message_tracking()
        
        # Show summary
        results.summary()
        
        return 0 if results.failed == 0 else 1
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

