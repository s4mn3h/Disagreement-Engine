# ============================================================
# DISAGREEMENT ENGINE
# Two AI voices, same question. One answers, one challenges.
# ============================================================

# STEP 1: Import the library that lets Python talk to Claude's API.
# Install first:  pip install anthropic
import anthropic

# STEP 2: Create a "client" — your connection to the API.
# It looks for your API key in an environment variable called
# ANTHROPIC_API_KEY. Set it once and forget it.
#
# Windows:    setx ANTHROPIC_API_KEY "your-key-here"
# Mac/Linux:  export ANTHROPIC_API_KEY="your-key-here"
# Then restart your terminal so it picks up the change.
client = anthropic.Anthropic()

# STEP 3: Pick a question to test.
# Change this to anything. Try things where you suspect
# an AI might be overconfident or miss something.
question = "Is nuclear energy the safest form of power generation?"

# STEP 4: Define what each "voice" does.
voice_one_instructions = """
Answer the user's question accurately and concisely.
State your confidence level at the end (high / medium / low).
If you're uncertain about anything, say so explicitly.
"""

voice_two_instructions = """
You are a critical reviewer. The user will show you a question
and an answer someone else gave. Your job is to:
- Find any errors, overstatements, or missing context
- Challenge weak reasoning
- Note if the confidence level seems justified
- Say "NO ISSUES FOUND" only if the answer is genuinely solid
Be specific. Don't nitpick for the sake of it.
"""

# ============================================================
# STEP 5: Voice One answers the question
# ============================================================

print("=" * 60)
print("QUESTION:", question)
print("=" * 60)
print()
print("--- VOICE ONE (Answerer) ---")
print()

response_one = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=voice_one_instructions,
    messages=[
        {"role": "user", "content": question}
    ]
)

answer_one = response_one.content[0].text
print(answer_one)

# ============================================================
# STEP 6: Voice Two challenges Voice One
# ============================================================

print()
print("--- VOICE TWO (Challenger) ---")
print()

challenge_prompt = f"""
ORIGINAL QUESTION: {question}

ANSWER GIVEN:
{answer_one}

Review this answer. Find problems if they exist.
"""

response_two = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=voice_two_instructions,
    messages=[
        {"role": "user", "content": challenge_prompt}
    ]
)

answer_two = response_two.content[0].text
print(answer_two)

# ============================================================
# DONE.
#
# TO RUN:
#   1. Open terminal
#   2. python disagreement_engine.py
#   3. Read both outputs, notice where they disagree
#
# NEXT STEPS:
#   - Try different questions
#   - Add a third voice that resolves disagreements
#   - Log results to a file for review
#   - Swap voice_two to a different model for genuine diversity
# ============================================================
