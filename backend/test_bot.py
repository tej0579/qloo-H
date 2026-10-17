import asyncio
import sys
sys.stdout.reconfigure(encoding="utf-8")
from app.bot import videogame_bot
from app.memory import memory_store

async def run_tests():
    print("\n================== TESTING ARCHITECTURE ==================")

    # Test 1: Step 0 Domain Guardrail Rollback
    print("\n[TEST 1] Step 0 Domain Guardrail Rollback...")
    sess_id = "test_guardrail"
    res = await videogame_bot.process_turn(sess_id, "How do I make chocolate cake?")
    print(f"Status: {res.status} | Turn: {res.turn} | Rollback: {res.is_rollback}")
    assert res.status == "ROLLBACK"
    assert res.turn == 0
    print("✓ Test 1 Passed: Off-topic query rejected.")

    # Test 1B: Step 0 Greeting & Meta questions (Must stay at Turn 0!)
    print("\n[TEST 1B] Step 0 Greeting & Meta check (Must stay at Turn 0)...")
    res_hi = await videogame_bot.process_turn("test_hi", "hi")
    assert res_hi.turn == 0, f"Expected turn 0 for 'hi', got {res_hi.turn}"
    assert "Hey there" in res_hi.message

    res_who = await videogame_bot.process_turn("test_who", "who are you bro")
    assert res_who.turn == 0, f"Expected turn 0 for 'who are you bro', got {res_who.turn}"
    print("✓ Test 1B Passed: 'hi' and 'who are you bro' correctly stay at Turn 0 without advancing steps.")

    # Test 2: Full 4-Turn Calibration Loop
    print("\n[TEST 2] Running Full 4-Turn Qloo Loop...")
    sess_id = "test_loop"
    memory_store.reset(sess_id)

    # Turn 1: Anchor Game
    print("\n-- Turn 1: Sending 'I love Elden Ring' --")
    r1 = await videogame_bot.process_turn(sess_id, "I love Elden Ring")
    print(f"Status: {r1.status} | Turn: {r1.turn}")
    print(f"Agent Counter-Prompt #1:\n{r1.message}\nOptions: {r1.counter_prompt.options}")
    assert r1.status == "SUCCESS"
    assert r1.turn == 1

    # Turn 2: Mechanics Answer
    print("\n-- Turn 2: Sending 'Tight combat mechanics & reflex mastery' --")
    r2 = await videogame_bot.process_turn(sess_id, "Tight combat mechanics & reflex mastery")
    print(f"Status: {r2.status} | Turn: {r2.turn}")
    print(f"Agent Counter-Prompt #2:\n{r2.message}\nOptions: {r2.counter_prompt.options}")
    assert r2.status == "SUCCESS"
    assert r2.turn == 2

    # Turn 3: Aesthetic Answer
    print("\n-- Turn 3: Sending 'Gritty, dark Gothic realism (3D immersive)' --")
    r3 = await videogame_bot.process_turn(sess_id, "Gritty, dark Gothic realism (3D immersive)")
    print(f"Status: {r3.status} | Turn: {r3.turn}")
    print(f"Agent Counter-Prompt #3:\n{r3.message}\nOptions: {r3.counter_prompt.options}")
    assert r3.status == "SUCCESS"
    assert r3.turn == 3

    # Turn 4: Platform & Length Answer -> Synthesis
    print("\n-- Turn 4: Sending 'PS5, tight 15 to 25 hours' --")
    r4 = await videogame_bot.process_turn(sess_id, "PS5, tight 15 to 25 hours")
    print(f"Status: {r4.status} | Turn: {r4.turn}")
    print(f"Final Grounded Synthesis:\n{r4.message}")
    assert r4.status == "COMPLETED"
    assert r4.turn == 4
    assert r4.final_synthesis is not None
    print("✓ Test 2 Passed: Full 4-turn loop successfully completed.")

    print("\n================== ALL TESTS PASSED ==================\n")

if __name__ == "__main__":
    asyncio.run(run_tests())
