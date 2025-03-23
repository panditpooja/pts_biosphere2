import subprocess

def ask_llm(prompt: str) -> str:
    """
    Calls Mistral using 'ollama run mistral' via CLI and returns the output.
    """
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt.encode("utf-8"),
            capture_output=True,
            timeout=90
        )
        return result.stdout.decode("utf-8").strip()
    except subprocess.TimeoutExpired:
        return "LLM Error: Timeout"
    except Exception as e:
        return f"LLM Error: {e}"


def build_prompt(alerts: dict, crop_health: dict) -> str:
    """
    Builds a clean, structured prompt for the LLM based on current system state.
    """
    prompt = "🌐 You are the AI manager for the Biosphere 2 environment.\n\n"
    prompt += "📡 Sensor Alerts:\n"
    if not alerts:
        prompt += "- No current alerts.\n"
    else:
        for key, value in alerts.items():
            prompt += f"- {key}: {value}\n"

    prompt += "\n🌿 Crop Health:\n"
    for crop, status in crop_health.items():
        prompt += f"- {crop}: {status}\n"

    prompt += "\n🎯 Choose actions (if needed) using one or more of the following:\n"
    prompt += "- Irrigate\n- Ventilate\n- Reroute\n"
    prompt += "Reply in plain language using these terms only if actions are needed.\n"
    return prompt


def parse_llm_actions(response: str) -> dict:
    """
    Parses LLM output to detect actionable commands.
    """
    response = response.lower()
    return {
        "irrigate": any(term in response for term in ["irrigate", "water", "humidity"]),
        "ventilate": any(term in response for term in ["ventilate", "air", "circulate"]),
        "reroute": any(term in response for term in ["reroute", "new goal", "change path"])
    }
