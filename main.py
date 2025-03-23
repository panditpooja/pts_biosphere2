import pygame
import sys
import time
import random
import pickle
import os
import threading

from sensor_interface import SensorInterface
from terrain_agent import TerrainGrid, Agent
from crop_health import evaluate_crop_health
from llm_reasoner import ask_llm, parse_llm_actions
from control_engine import apply_ai_actions
from twin_overlay import draw_overlay

# --- Setup ---
pygame.init()
CELL_SIZE = 60
GRID_SIZE = 10
SCREEN_SIZE = GRID_SIZE * CELL_SIZE
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + 120))
pygame.display.set_caption("Biosphere 2 Twin AI Simulator")
clock = pygame.time.Clock()

# --- Init core components ---
sensor = SensorInterface("C:/Users/ual-laptop/Downloads/B2Twin-Hackathon-main/B2Twin-Hackathon-main/data")
sensor.reset()
terrain = TerrainGrid()
agent = Agent(terrain)

# RL Q-table
Q_PATH = "q_table.pkl"
q_table = {}
if os.path.exists(Q_PATH):
    with open(Q_PATH, "rb") as f:
        q_table = pickle.load(f)

learning_rate = 0.1
discount = 0.95
epsilon = 1.0
epsilon_decay = 0.995
epsilon_min = 0.01

score = 0
irrigation_on = False
llm_response = {"text": "Awaiting reasoning..."}
ACTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # left, right, up, down

max_episodes = 10
max_steps = 300

for episode in range(max_episodes):
    print(f"\n🚀 Episode {episode+1}/{max_episodes}")
    agent.reset()
    terrain.reset()
    sensor.reset()
    forced_prompt = True
    score = 0

    for step in range(max_steps):
        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        state = agent.state
        if random.random() < epsilon:
            action = random.choice(ACTIONS)
        else:
            q_values = [q_table.get((state, a), 0) for a in ACTIONS]
            max_q = max(q_values)
            best_actions = [a for a, q in zip(ACTIONS, q_values) if q == max_q]
            action = random.choice(best_actions)

        agent.step(action)
        next_state = agent.state

        # --- Reward ---
        if next_state == agent.goal:
            reward = 50
        elif not terrain.is_valid(next_state):
            reward = -10
        else:
            reward = -1

        old_q = q_table.get((state, action), 0.0)
        next_max = max([q_table.get((next_state, a), 0) for a in ACTIONS])
        new_q = old_q + learning_rate * (reward + discount * next_max - old_q)
        q_table[(state, action)] = new_q

        frame = sensor.get_next_sensor_frame()
        if frame is None:
            print("✅ Sensor data finished.")
            break

        alerts = sensor.get_active_alerts(frame, {
            "Desert_CO2_FEB-2025__CO2_desert[ppm]": (200, 1000),
            "RF_MountainTower_Temp_FEB-2025__Temp_13m[degC]": (10, 35),
            "RF_TigerPond_Temp_RH_FEB-2025__RH[%]": (30, 80)
        })

        crop_status = evaluate_crop_health(frame, terrain.crop_zones)

        # Async LLM trigger on alerts
        def call_llm():
            try:
                prompt = f"Sensor alert: {alerts}. Crop health: {crop_status}. What should we do?"
                print(f"🧠 Prompt sent to LLM:\n{prompt}")
                llm_response["text"] = ask_llm(prompt)
                print("💬 LLM Response:\n", llm_response["text"])
                actions = parse_llm_actions(llm_response["text"])
                apply_ai_actions(actions, agent, terrain)
            except Exception as e:
                llm_response["text"] = f"LLM error: {e}"

        if alerts or forced_prompt:
            forced_prompt = False
            llm_response["text"] = "🤖 Thinking..."
            thread = threading.Thread(target=call_llm)
            thread.start()

        if any("🥀" in status for status in crop_status.values()):
            score -= 5
        else:
            score += 1

        # --- Draw Grid ---
        screen.fill((255, 255, 255))
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                color = (200, 255, 200)
                if (x, y) == agent.state:
                    color = (255, 165, 0)
                elif (x, y) == agent.goal:
                    color = (255, 255, 0)
                elif (x, y) in terrain.obstacles:
                    color = (255, 0, 0)
                elif (x, y) in terrain.crop_zones:
                    color = (139, 69, 19)
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, (0, 0, 0), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        draw_overlay(screen, frame, alerts, llm_response["text"], crop_status, score, irrigation_on)
        pygame.display.flip()
        clock.tick(5)

        if next_state == agent.goal:
            print(f"✅ Reached goal in {step+1} steps!")
            break

    epsilon = max(epsilon * epsilon_decay, epsilon_min)

# Save Q-table after training
with open(Q_PATH, "wb") as f:
    pickle.dump(q_table, f)

print("🏁 Training complete. Q-table saved.")
pygame.quit()
sys.exit()
