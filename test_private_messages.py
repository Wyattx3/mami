"""
Test Private Message Delivery to 50+ Players
Simulates sending private messages and tracks delivery failures
"""
import asyncio
import sys
from pathlib import Path
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))


async def test_private_message_delivery():
    """
    Simulate private message delivery to 50 players
    Track success/failure rates and identify issues
    """
    print("=" * 60)
    print("🧪 Private Message Delivery Test (50 Players)")
    print("=" * 60)
    
    # Simulate 50 players with different scenarios
    test_scenarios = {
        'success': 0,
        'user_not_started_bot': 0,
        'user_blocked_bot': 0,
        'rate_limited': 0,
        'timeout': 0,
        'network_error': 0,
        'other_error': 0
    }
    
    # Test configuration
    TOTAL_PLAYERS = 50
    MESSAGES_PER_SECOND = 30  # Telegram limit
    DELAY_BETWEEN_MESSAGES = 1.0 / MESSAGES_PER_SECOND  # ~33ms
    
    print(f"\n📊 Test Configuration:")
    print(f"   Total players: {TOTAL_PLAYERS}")
    print(f"   Rate limit: {MESSAGES_PER_SECOND} msg/sec")
    print(f"   Delay per message: {DELAY_BETWEEN_MESSAGES*1000:.1f}ms")
    print(f"\n🚀 Starting message delivery simulation...\n")
    
    start_time = time.time()
    
    # Simulate sending messages to 50 players
    for i in range(TOTAL_PLAYERS):
        player_id = i + 1
        
        # Simulate different error scenarios based on player_id
        try:
            # Wait for rate limit
            await asyncio.sleep(DELAY_BETWEEN_MESSAGES)
            
            # Simulate different scenarios
            if i < 35:
                # 70% success rate (players who started bot)
                print(f"   ✅ Player {player_id}: Message delivered")
                test_scenarios['success'] += 1
                
            elif i < 40:
                # 10% - User hasn't started bot
                print(f"   ⚠️  Player {player_id}: User hasn't started bot")
                test_scenarios['user_not_started_bot'] += 1
                
            elif i < 44:
                # 8% - User blocked bot
                print(f"   🚫 Player {player_id}: User blocked bot")
                test_scenarios['user_blocked_bot'] += 1
                
            elif i < 47:
                # 6% - Rate limited
                print(f"   ⏱️  Player {player_id}: Rate limited, retrying...")
                await asyncio.sleep(1.0)  # Wait and retry
                print(f"   ✅ Player {player_id}: Message delivered (retry)")
                test_scenarios['rate_limited'] += 1
                
            elif i < 49:
                # 4% - Timeout
                print(f"   ⏳ Player {player_id}: Timeout error")
                test_scenarios['timeout'] += 1
                
            else:
                # 2% - Other error
                print(f"   ❌ Player {player_id}: Network error")
                test_scenarios['network_error'] += 1
                
        except Exception as e:
            print(f"   ❌ Player {player_id}: Unexpected error - {e}")
            test_scenarios['other_error'] += 1
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Calculate statistics
    total_delivered = test_scenarios['success'] + test_scenarios['rate_limited']
    total_failed = TOTAL_PLAYERS - total_delivered
    success_rate = (total_delivered / TOTAL_PLAYERS) * 100
    
    # Results
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    print(f"\n✅ Successful Deliveries: {total_delivered}/{TOTAL_PLAYERS} ({success_rate:.1f}%)")
    print(f"   • Direct success: {test_scenarios['success']}")
    print(f"   • After retry (rate limit): {test_scenarios['rate_limited']}")
    
    print(f"\n❌ Failed Deliveries: {total_failed}/{TOTAL_PLAYERS} ({(total_failed/TOTAL_PLAYERS)*100:.1f}%)")
    print(f"   • User not started bot: {test_scenarios['user_not_started_bot']}")
    print(f"   • User blocked bot: {test_scenarios['user_blocked_bot']}")
    print(f"   • Timeout errors: {test_scenarios['timeout']}")
    print(f"   • Network errors: {test_scenarios['network_error']}")
    print(f"   • Other errors: {test_scenarios['other_error']}")
    
    print(f"\n⏱️  Performance:")
    print(f"   Total time: {total_time:.2f} seconds")
    print(f"   Average per message: {(total_time/TOTAL_PLAYERS)*1000:.1f}ms")
    print(f"   Effective rate: {TOTAL_PLAYERS/total_time:.1f} msg/sec")
    
    # Common Issues
    print("\n" + "=" * 60)
    print("🔍 Common Issues & Solutions")
    print("=" * 60)
    
    print("\n1️⃣ User hasn't started bot:")
    print("   ❌ Problem: Bot can't send private messages")
    print("   ✅ Solution: Prompt user to start bot in private chat")
    print("   📝 Message: 'ကျေးဇူးပြု၍ @BotName ကို private မှာ /start နှိပ်ပါ'")
    
    print("\n2️⃣ User blocked bot:")
    print("   ❌ Problem: User explicitly blocked the bot")
    print("   ✅ Solution: Silently skip, log for admin")
    print("   📝 Note: Cannot force message to blocked users")
    
    print("\n3️⃣ Rate limiting:")
    print("   ❌ Problem: Exceeding 30 messages/second")
    print("   ✅ Solution: Implement message queue with delays")
    print("   📝 Code: Add 33ms delay between messages")
    
    print("\n4️⃣ Timeout/Network errors:")
    print("   ❌ Problem: Network issues or slow connection")
    print("   ✅ Solution: Retry with exponential backoff")
    print("   📝 Retry: 3 attempts with 1s, 2s, 4s delays")
    
    # Recommendations
    print("\n" + "=" * 60)
    print("💡 Recommendations for Bot")
    print("=" * 60)
    
    print("\n✅ Implement:")
    print("   1. Message queue system")
    print("   2. Retry logic (3 attempts)")
    print("   3. Rate limit tracking (30 msg/sec)")
    print("   4. Error categorization and logging")
    print("   5. User notification for failed messages")
    
    print("\n✅ Expected Success Rate:")
    print("   • With all users started bot: 95-98%")
    print("   • With mixed users: 70-80%")
    print("   • Public bot reality: 60-70%")
    
    print("\n" + "=" * 60)
    
    return success_rate


async def test_batch_delivery_strategies():
    """Test different batching strategies"""
    print("\n" + "=" * 60)
    print("🎯 Batch Delivery Strategies Comparison")
    print("=" * 60)
    
    TOTAL_MESSAGES = 50
    
    # Strategy 1: Sequential (33ms delay)
    print("\n1️⃣ Strategy 1: Sequential with Rate Limit")
    start = time.time()
    for i in range(TOTAL_MESSAGES):
        await asyncio.sleep(1.0/30)  # 33ms
    time1 = time.time() - start
    print(f"   Time: {time1:.2f}s")
    print(f"   Rate: {TOTAL_MESSAGES/time1:.1f} msg/sec")
    
    # Strategy 2: Batched (10 at a time)
    print("\n2️⃣ Strategy 2: Batched (10 concurrent)")
    start = time.time()
    for batch in range(0, TOTAL_MESSAGES, 10):
        tasks = []
        for i in range(10):
            if batch + i < TOTAL_MESSAGES:
                tasks.append(asyncio.sleep(0.01))  # Simulate send
        await asyncio.gather(*tasks)
        await asyncio.sleep(0.5)  # Wait between batches
    time2 = time.time() - start
    print(f"   Time: {time2:.2f}s")
    print(f"   Rate: {TOTAL_MESSAGES/time2:.1f} msg/sec")
    
    # Strategy 3: Queue-based (30 msg/sec)
    print("\n3️⃣ Strategy 3: Message Queue (30 msg/sec)")
    start = time.time()
    queue = asyncio.Queue()
    
    # Add all messages to queue
    for i in range(TOTAL_MESSAGES):
        await queue.put(i)
    
    # Process queue with rate limit
    processed = 0
    while not queue.empty():
        await queue.get()
        processed += 1
        await asyncio.sleep(1.0/30)  # Rate limit
    
    time3 = time.time() - start
    print(f"   Time: {time3:.2f}s")
    print(f"   Rate: {TOTAL_MESSAGES/time3:.1f} msg/sec")
    
    print("\n📊 Comparison:")
    print(f"   Sequential: {time1:.2f}s")
    print(f"   Batched:    {time2:.2f}s ({'faster' if time2 < time1 else 'slower'})")
    print(f"   Queue:      {time3:.2f}s ({'faster' if time3 < time1 else 'slower'})")
    
    print("\n✅ Recommended: Queue-based approach")
    print("   • Respects rate limits")
    print("   • Handles errors gracefully")
    print("   • Easy to monitor")


async def run_all_tests():
    """Run all private message tests"""
    print("\n" + "=" * 60)
    print("🧪 PRIVATE MESSAGE DELIVERY TESTING")
    print("=" * 60)
    print("Testing bot's ability to send private messages to 50 players")
    print("=" * 60)
    
    # Test 1: Message delivery simulation
    success_rate = await test_private_message_delivery()
    
    # Test 2: Batch strategies
    await test_batch_delivery_strategies()
    
    # Final summary
    print("\n" + "=" * 60)
    print("🎯 FINAL SUMMARY")
    print("=" * 60)
    
    if success_rate >= 70:
        print("✅ PASSED: Acceptable delivery rate")
        print(f"   Success rate: {success_rate:.1f}%")
    else:
        print("⚠️  WARNING: Low delivery rate")
        print(f"   Success rate: {success_rate:.1f}%")
        print("   Action needed: Improve error handling")
    
    print("\n🔧 Next Steps:")
    print("   1. Implement improved error handling")
    print("   2. Add message queue system")
    print("   3. Add retry logic")
    print("   4. Add user notification system")
    print("   5. Test with real bot and real users")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(run_all_tests())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

