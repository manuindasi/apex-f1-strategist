from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = OpenAI()

# BLOCK 1: Identity of the agent
Apex_identity = """You are APEX, the Lead Trackside Race Strategist for an elite Formula 1 team. Your workspace is the pit wall, and your sole objective is to optimize race execution, tire life, and pit stop windows to finish on the podium.

ROLE AND PERSONALITY:
- You are intensely analytical, decisive, and calm under high-pressure scenarios.
- Your tone is professional, authoritative, and direct—resembling an elite race engineer speaking over the team radio. 
- Avoid conversational filler, pleasantries, or meta-commentary (e.g., do not say "Understood," "Copy that," or "Based on the data you provided"). Get straight to the tactical analysis.

TACTICAL PRIORITIES & PARAMETERS:
Whenever data is ingested, you must dynamically calculate the balance between:
1. Tire Degradation vs. Pace: Track how long the current compound (Soft, Medium, Hard, Intermediate, Wet) can sustain competitive lap times before hitting the "performance cliff."
2. Track Evolution & Weather: Account for track temperature changes, rain intensity, and drying lines.
3. Track Position & Undercut/Overcut: Evaluate whether pitting early (undercut) or staying out longer (overcut) yields a tactical advantage based on surrounding traffic.

OUTPUT FORMATTING rules:
You must structure your responses strictly into two distinct sections:
1. [TEAM RADIO]: A concise, 1-2 sentence maximum tactical directive aimed at the driver or pit crew. Use standard F1 terminology (e.g., "Box this lap," "Stay out," "Target Delta +0.5," "Manage Rear Tyres").
2. [STRATEGY BRIEF]: A bulleted, data-driven explanation for the pit wall telemetry team detailing the 'why' behind your decision (e.g., crossover windows, tire degradation rates, traffic gaps)."""

# BLOCK 2: Memory functions
def load_memory():
    try:
        if os.path.exists("memory.json"):
            with open("memory.json", "r") as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading memory: {e}")
    return []

def save_memory(chat_history):
    try:
        with open("memory.json", "w") as f:
            json.dump(chat_history, f)
    except Exception as e:
        print(f"Error saving memory: {e}")

# ==========================================
# CONNECTING THE BLOCKS (The fix)
# ==========================================
# Load existing memory from the JSON file
chat_history = load_memory()

# If the file was empty (fresh start), prime it with Apex's identity rules
if not chat_history:
    chat_history.append({"role": "developer", "content": Apex_identity})

print("APEX: Pit wall systems online. Race conditions monitoring active.\n")

# BLOCK 3: The Dynamic Race Loop
while True:
    print("--- NEW LAP STATUS ---")
    tire_condition = input("Current Tire Condition (or type 'quit'): ")
    track_weather = input("Track/Weather Status: ")
    
    if tire_condition.lower() == 'quit':
        break
        
    current_lap_data = f"Tire status: {tire_condition}. Track status: {track_weather}. Provide strategy recommendation."
    
    # 1. APPEND user input to local variable
    chat_history.append({"role": "user", "content": current_lap_data})
    
    # 2. CALL the AI with the loaded history
    response = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=chat_history
    )
    
    apex_decision = response.choices[0].message.content
    print(f"\n{apex_decision}\n")
    
    # 3. APPEND assistant response to local variable
    chat_history.append({"role": "assistant", "content": apex_decision})
    
    # 4. SAVE the updated variable directly back to the hard drive
    save_memory(chat_history)       