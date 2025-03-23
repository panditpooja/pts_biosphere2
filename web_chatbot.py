from flask import Flask, request, jsonify
from flask_cors import CORS
from sensor_interface import SensorInterface
from crop_health import evaluate_crop_health
from llm_reasoner import ask_llm, build_prompt, parse_llm_actions

app = Flask(__name__)
CORS(app)

# ✅ Load sensor data only once per session
sensor = SensorInterface("C:/Users/ual-laptop/Downloads/B2Twin-Hackathon-main/B2Twin-Hackathon-main/data")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # ✅ Get next frame
        frame = sensor.get_next_sensor_frame()
        if frame is None:
            return jsonify({"error": "✅ Sensor data exhausted."}), 200

        # ✅ Detect alerts
        alerts = sensor.get_active_alerts(frame, {
            "Desert_CO2_FEB-2025__CO2_desert[ppm]": (200, 1000),
            "RF_MountainTower_Temp_FEB-2025__Temp_13m[degC]": (10, 35),
            "RF_TigerPond_Temp_RH_FEB-2025__RH[%]": (30, 80)
        })

        # ✅ Crop health
        crop_status = evaluate_crop_health(frame, {
            (2, 2): "Tomatoes",
            (5, 5): "Corn",
            (7, 8): "Lettuce"
        })

        # ✅ Build and send prompt to LLM
        prompt = build_prompt(alerts, crop_status)
        print("\n🧠 Prompt to LLM:\n", prompt)

        reasoning = ask_llm(prompt)
        print("\n💬 LLM Response:\n", reasoning)

        actions = parse_llm_actions(reasoning)
        print("✅ Parsed Actions:", actions)

        return jsonify({
            "prompt": prompt,
            "reasoning": reasoning,
            "actions": actions,
            "alerts": alerts,
            "crop_status": crop_status
        }), 200

    except Exception as e:
        print("❌ Error in /chat:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
