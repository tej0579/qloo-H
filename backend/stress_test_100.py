import asyncio
import sys
from typing import List, Dict, Any

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from app.bot import videogame_bot
from app.memory import memory_store

async def run_100_stress_tests():
    print("=" * 80)
    print("STARTING 100-LOOP STRESS TEST SUITE FOR QLOO VIDEOGAME CULTURAL AGENT")
    print("=" * 80)

    passed_count = 0
    failed_count = 0
    failures = []

    # Helper to test a single step
    async def test_step(loop_num: int, session_id: str, prompt: str, expected_turn: int, expected_status: str, check_fn=None):
        nonlocal passed_count, failed_count
        try:
            res = await videogame_bot.process_turn(session_id, prompt)
            turn_ok = (res.turn == expected_turn)
            status_ok = (res.status == expected_status)
            custom_ok = check_fn(res) if check_fn else True

            if turn_ok and status_ok and custom_ok:
                passed_count += 1
                status_str = "PASS"
            else:
                failed_count += 1
                status_str = "FAIL"
                failures.append({
                    "loop": loop_num,
                    "prompt": prompt,
                    "expected_turn": expected_turn,
                    "actual_turn": res.turn,
                    "expected_status": expected_status,
                    "actual_status": res.status,
                    "message": res.message[:120]
                })

            print(f"[{loop_num:3d}/100] [{status_str}] Turn {res.turn} | Status: {res.status:9s} | Prompt: \"{prompt[:35]}\"")
            return res
        except Exception as e:
            failed_count += 1
            print(f"[{loop_num:3d}/100] [ERROR] Prompt: \"{prompt[:35]}\" -> Exception: {e}")
            failures.append({
                "loop": loop_num,
                "prompt": prompt,
                "error": str(e)
            })
            return None

    # ================= LOOPS 1 - 10: Acronyms & Short Game Titles =================
    print("\n--- BATCH 1: Acronyms & Aliases (Loops 1 - 10) ---")
    acronym_tests = [
        ("gta 5", "Grand Theft Auto"),
        ("gta v", "Grand Theft Auto"),
        ("rdr2", "Red Dead Redemption"),
        ("cod", "Call of Duty"),
        ("gow", "God of War"),
        ("bg3", "Baldur's Gate"),
        ("cs2", "Counter-Strike"),
        ("tf2", "Team Fortress"),
        ("ff7", "Final Fantasy"),
        ("eldenring", "Elden Ring")
    ]
    for i, (acronym, expected_name) in enumerate(acronym_tests, start=1):
        s_id = f"stress_alias_{i}"
        await test_step(
            loop_num=i,
            session_id=s_id,
            prompt=acronym,
            expected_turn=1,
            expected_status="SUCCESS",
            check_fn=lambda r, name=expected_name: name.lower() in (r.qloo_data.get("anchor", {}).get("name", "").lower() if r.qloo_data else "")
        )

    # ================= LOOPS 11 - 20: Genre Scouting Inquiries at Turn 0 =================
    print("\n--- BATCH 2: Genre Scouting at Turn 0 (Loops 11 - 20) ---")
    genre_tests = [
        "suggest some fpp games",
        "fpp games",
        "fps",
        "horror games",
        "rpg games",
        "racing games",
        "co-op games",
        "souls like",
        "open world games",
        "stealth games"
    ]
    for i, prompt in enumerate(genre_tests, start=11):
        s_id = f"stress_genre_{i}"
        await test_step(
            loop_num=i,
            session_id=s_id,
            prompt=prompt,
            expected_turn=0,
            expected_status="SUCCESS",
            check_fn=lambda r: r.counter_prompt is not None and len(r.counter_prompt.options) >= 3
        )

    # ================= LOOPS 21 - 30: Greetings & Meta Questions at Turn 0 =================
    print("\n--- BATCH 3: Greetings & Meta Inquiries at Turn 0 (Loops 21 - 30) ---")
    meta_tests = [
        "hi",
        "hello",
        "hey there",
        "who are you",
        "where are you from",
        "are you a bot",
        "what can you do",
        "wassup",
        "good evening",
        "who made you"
    ]
    for i, prompt in enumerate(meta_tests, start=21):
        s_id = f"stress_meta_{i}"
        await test_step(
            loop_num=i,
            session_id=s_id,
            prompt=prompt,
            expected_turn=0,
            expected_status="SUCCESS",
            check_fn=lambda r: len(r.message) > 20
        )

    # ================= LOOPS 31 - 40: Domain Guardrail / Off-Topic Attacks =================
    print("\n--- BATCH 4: Off-Topic Guardrails (Loops 31 - 40) ---")
    offtopic_tests = [
        "make me a pizza recipe",
        "who won the presidential election",
        "what is the weather forecast today",
        "should I invest in bitcoin and crypto",
        "solve x^2 + 5x + 6 = 0 calculus",
        "write a javascript react component",
        "symptoms of acute fever doctor",
        "book a cheap flight ticket to new york",
        "how to bake a chocolate cake",
        "what is your stock portfolio dividend"
    ]
    for i, prompt in enumerate(offtopic_tests, start=31):
        s_id = f"stress_guardrail_{i}"
        await test_step(
            loop_num=i,
            session_id=s_id,
            prompt=prompt,
            expected_turn=0,
            expected_status="ROLLBACK",
            check_fn=lambda r: r.is_rollback and "Domain Guardrail" in r.message
        )

    # ================= LOOPS 41 - 55: Multi-Turn End-to-End Calibrations =================
    print("\n--- BATCH 5: Full 4-Turn Calibration Sequences (Loops 41 - 55) ---")
    # Flow 1: Elden Ring (Loops 41-44)
    flow1_s = "flow_elden_ring"
    await test_step(41, flow1_s, "Elden Ring", 1, "SUCCESS")
    await test_step(42, flow1_s, "Tight combat mechanics and reflex mastery", 2, "SUCCESS")
    await test_step(43, flow1_s, "Gritty Gothic realism and dark ruins", 3, "SUCCESS")
    await test_step(44, flow1_s, "PS5, tight 15 to 25 hours campaign", 4, "COMPLETED",
                    check_fn=lambda r: r.final_synthesis is not None and "recommendations" in r.final_synthesis)

    # Flow 2: Cyberpunk 2077 (Loops 45-48)
    flow2_s = "flow_cyberpunk"
    await test_step(45, flow2_s, "Cyberpunk 2077", 1, "SUCCESS")
    await test_step(46, flow2_s, "Deep build variety, theorycrafting & RPG progression", 2, "SUCCESS")
    await test_step(47, flow2_s, "Sci-fi / futuristic dystopian aesthetic", 3, "SUCCESS")
    await test_step(48, flow2_s, "PC, massive 60-100+ hour open-world epic", 4, "COMPLETED",
                    check_fn=lambda r: r.final_synthesis is not None and len(r.final_synthesis.get("recommendations", [])) >= 2)

    # Flow 3: Hades (Loops 49-52)
    flow3_s = "flow_hades"
    await test_step(49, flow3_s, "Hades", 1, "SUCCESS")
    await test_step(50, flow3_s, "Tight reflex combat mastery", 2, "SUCCESS")
    await test_step(51, flow3_s, "Stylized, atmospheric indie world (2D / Isometric)", 3, "SUCCESS")
    await test_step(52, flow3_s, "Nintendo Switch / Steam Deck portable", 4, "COMPLETED",
                    check_fn=lambda r: r.final_synthesis is not None)

    # Flow 4: Partial Grand Theft Auto V (Loops 53-55)
    flow4_s = "flow_gta5"
    await test_step(53, flow4_s, "gta 5", 1, "SUCCESS")
    await test_step(54, flow4_s, "Atmospheric exploration and storyline", 2, "SUCCESS")
    await test_step(55, flow4_s, "3D realistic open world", 3, "SUCCESS")

    # ================= LOOPS 56 - 70: In-Loop Interruptions & Distractions =================
    print("\n--- BATCH 6: In-Loop Meta & Greeting Interruptions (Loops 56 - 70) ---")
    interrupt_s1 = "inter_s1"
    await videogame_bot.process_turn(interrupt_s1, "Elden Ring") # Now Turn 1
    # Test interruptions at Turn 1 (Loops 56 - 60)
    for i, prompt in enumerate(["hi", "who are you", "where are you from", "are you an ai", "hello there"], start=56):
        await test_step(
            loop_num=i,
            session_id=interrupt_s1,
            prompt=prompt,
            expected_turn=1,
            expected_status="SUCCESS",
            check_fn=lambda r: r.counter_prompt is not None and "Tight combat" in r.counter_prompt.options[0]
        )

    # Advance to Turn 2
    await videogame_bot.process_turn(interrupt_s1, "Tight combat mechanics") # Now Turn 2
    # Test interruptions at Turn 2 (Loops 61 - 65)
    for i, prompt in enumerate(["what can you do", "yo", "where do you live", "whats up", "who made you"], start=61):
        await test_step(
            loop_num=i,
            session_id=interrupt_s1,
            prompt=prompt,
            expected_turn=2,
            expected_status="SUCCESS",
            check_fn=lambda r: r.counter_prompt is not None
        )

    # Advance to Turn 3
    await videogame_bot.process_turn(interrupt_s1, "Gritty 3D Gothic realism") # Now Turn 3
    # Test interruptions at Turn 3 (Loops 66 - 70)
    for i, prompt in enumerate(["hi there", "can you help me", "who are you again", "hello", "sup"], start=66):
        await test_step(
            loop_num=i,
            session_id=interrupt_s1,
            prompt=prompt,
            expected_turn=3,
            expected_status="SUCCESS",
            check_fn=lambda r: r.counter_prompt is not None and "PC, tight" in r.counter_prompt.options[0]
        )

    # ================= LOOPS 71 - 80: Vague & Nonsense Answers in Calibration =================
    print("\n--- BATCH 7: Vague Calibration Rejections (Loops 71 - 80) ---")
    vague_s = "vague_session"
    await videogame_bot.process_turn(vague_s, "Cyberpunk 2077") # Now Turn 1
    vague_inputs = ["k", "yes", "no", "idk", "why", "dunno", "cool", "fine", "what", "ok"]
    for i, vague_word in enumerate(vague_inputs, start=71):
        await test_step(
            loop_num=i,
            session_id=vague_s,
            prompt=vague_word,
            expected_turn=1,
            expected_status="SUCCESS",
            check_fn=lambda r: "more specific" in r.message
        )

    # ================= LOOPS 81 - 90: Prefixes, Casing & Punctuation Cleanup =================
    print("\n--- BATCH 8: Prefixes, Casing & Punctuation Formatting (Loops 81 - 90) ---")
    formatting_tests = [
        "i love Elden Ring",
        "I LIKE Hades",
        "games like Cyberpunk 2077",
        "something like Bloodborne",
        "ELDEN RING!!!",
        "  cyberpunk 2077  ",
        "best games like God of War",
        "recommend like Lies of P",
        "I play Hades.",
        "similar to Sekiro"
    ]
    for i, prompt in enumerate(formatting_tests, start=81):
        s_id = f"format_sess_{i}"
        await test_step(
            loop_num=i,
            session_id=s_id,
            prompt=prompt,
            expected_turn=1,
            expected_status="SUCCESS",
            check_fn=lambda r: r.qloo_data is not None and "anchor" in r.qloo_data
        )

    # ================= LOOPS 91 - 95: Session Resets =================
    print("\n--- BATCH 9: Reset & Start Over Commands (Loops 91 - 95) ---")
    reset_words = ["reset", "restart", "start over", "clear", "/reset"]
    for i, word in enumerate(reset_words, start=91):
        s_id = f"reset_sess_{i}"
        # Advance to Turn 2 first
        await videogame_bot.process_turn(s_id, "Elden Ring")
        await videogame_bot.process_turn(s_id, "Tight combat mechanics")
        # Now reset
        await test_step(
            loop_num=i,
            session_id=s_id,
            prompt=word,
            expected_turn=0,
            expected_status="SUCCESS",
            check_fn=lambda r: "reset" in r.message.lower()
        )

    # ================= LOOPS 96 - 100: Corner Cases & Single Digits / Stopwords =================
    print("\n--- BATCH 10: Corner Cases & Single Digits (Loops 96 - 100) ---")
    # Loop 96: Standalone digit "5" should NOT match "Yakuza 5"
    s96 = "corner_96"
    await test_step(
        96, s96, "5", 0, "NOT_FOUND",
        check_fn=lambda r: "Could not find" in r.message
    )

    # Loop 97: Stopwords only "the game" should NOT match random entity
    s97 = "corner_97"
    await test_step(
        97, s97, "the game", 0, "NOT_FOUND",
        check_fn=lambda r: "Could not find" in r.message
    )

    # Loop 98: Question mark conversational "is this working?"
    s98 = "corner_98"
    await test_step(
        98, s98, "is this working?", 0, "SUCCESS",
        check_fn=lambda r: "cultural gaming agent" in r.message.lower() or "qloo" in r.message.lower()
    )

    # Loop 99: Alias "rdr" -> Red Dead Redemption
    s99 = "corner_99"
    await test_step(
        99, s99, "rdr", 1, "SUCCESS",
        check_fn=lambda r: "red dead" in r.qloo_data["anchor"]["name"].lower()
    )

    # Loop 100: Alias "cp2077" -> Cyberpunk 2077
    s100 = "corner_100"
    await test_step(
        100, s100, "cp2077", 1, "SUCCESS",
        check_fn=lambda r: "cyberpunk" in r.qloo_data["anchor"]["name"].lower()
    )

    print("\n" + "=" * 80)
    print(f"STRESS TEST COMPLETE: {passed_count}/100 PASSED | {failed_count}/100 FAILED")
    print("=" * 80)

    if failures:
        print("\nSUMMARY OF FAILURES:")
        for f in failures:
            print(f)
    else:
        print("\nALL 100 STRESS TEST LOOPS PASSED PERFECTLY!")

if __name__ == "__main__":
    asyncio.run(run_100_stress_tests())
