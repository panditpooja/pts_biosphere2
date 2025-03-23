import pygame

def draw_overlay(screen, frame, alerts, reasoning, crop_status, score, irrigation_on):
    font = pygame.font.SysFont("consolas", 18)
    overlay_rect = pygame.Rect(0, screen.get_height() - 120, screen.get_width(), 120)
    pygame.draw.rect(screen, (245, 245, 245), overlay_rect)
    pygame.draw.line(screen, (0, 0, 0), (0, overlay_rect.top), (screen.get_width(), overlay_rect.top), 2)

    lines = []
    lines.append(f"Score: {score}    Irrigation: {'ON' if irrigation_on else 'OFF'}")

    if alerts:
        lines.append("⚠️ Alerts:")
        for key, msg in alerts.items():
            lines.append(f"- {key}: {msg}")
    else:
        lines.append("✅ No alerts")

    if crop_status:
        unhealthy = [f"{k}: {v}" for k, v in crop_status.items() if "🥀" in v or "⚠️" in v]
        if unhealthy:
            lines.append("🌾 Crop Issues:")
            lines.extend([f"- {line}" for line in unhealthy])

    if reasoning:
        reasoning_lines = reasoning.strip().split("\n")[:4]  # show first 4 lines of reasoning
        lines.append("🧠 LLM Reasoning:")
        lines.extend([f"> {line.strip()}" for line in reasoning_lines if line.strip()])

    for i, text in enumerate(lines):
        rendered = font.render(text, True, (0, 0, 0))
        screen.blit(rendered, (10, overlay_rect.top + 10 + i * 20))
