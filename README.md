# Biosphere 2 Digital Twin AI

**An AI-powered, real-time digital twin simulation of the Biosphere 2 ecosystem**, integrating sensor data, crop health analysis, autonomous terrain navigation, and a local LLM-based decision-making interface.

## Project Overview

This project simulates a digital twin of **Biosphere 2**, using real sensor data and reinforcement learning to:

- Monitor **crop health** using environmental metrics (CO₂, PAR, Temp, RH)
- Navigate a 2D terrain with an **RL-trained agent** avoiding obstacles and reaching crop zones
- Use **Local LLM Reasoning** to decide when to irrigate, ventilate, or reroute paths based on sensor alerts
- Provide both a **visual simulation** (via Pygame) and a **chat interface** (via FastAPI + HTML)

---

## Key Features

| Feature               | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| Sensor Fusion       | Aggregates real-time CSV sensor streams (CO₂, Temp, PAR, RH)                  |
| LLM Reasoner        | Connects to a local LLM (via [Ollama](https://ollama.com)) for reasoning       |
| Terrain Agent       | RL-trained agent (Q-learning) navigates terrain with crops and obstacles       |
| Crop Health Engine  | Evaluates crops (Tomatoes, Corn) and color-codes health status                |
| Web Chatbot         | Ask questions to the Digital Twin and get AI-backed recommendations           |
| Overlay UI          | Real-time simulation with visual feedback (alerts, AI thoughts, health)       |

---

## Code Structure

├── main.py                # Runs the simulation loop (Pygame + Q-Learning + Sensor + AI)<br>
├── sensor_interface.py    # Loads and streams real Biosphere 2 sensor CSVs<br>
├── crop_health.py         # Scores and colorizes crop health based on environmental factors<br>
├── terrain_agent.py       # RL agent logic and terrain generation<br>
├── control_engine.py      # Applies AI-driven actions (irrigate, ventilate, reroute)<br>
├── llm_reasoner.py        # Interacts with local LLM (Ollama) and parses reasoning<br>
├── twin_overlay.py        # Renders UI overlays in simulation window<br>
├── web_chatbot.py         # FastAPI-powered chatbot for user-AI interaction<br>
├── q_table.pkl            # Q-learning knowledge base (auto-generated)<br>

---

## AI + RL Architecture

- **Reinforcement Learning (Q-Learning)** trains the agent to reach crops efficiently.
- **Local LLM** (like Mistral via Ollama) interprets sensor alerts and recommends actions.
- **AI actions** are parsed, applied, and reflected live in both the simulation and the web chatbot.

---

## Getting Started

### Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com) installed locally to run LLMs like `mistral`

### Install Dependencies

```bash
pip install pygame fastapi uvicorn pandas

---
🤖 Pull the LLM Model
bash
Copy
Edit
ollama pull mistral
▶️ Run the Simulator (Pygame Visualization)
bash
Copy
Edit
python main.py

---
💬 Launch the Web Chat Interface
bash
Copy
Edit
python web_chatbot.py
Then open your browser and visit: http://127.0.0.1:8080




