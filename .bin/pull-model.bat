@echo off
echo Downloading local AI model (kwangsuklee/Qwen3.5-4B-Claude-4.6-Opus-Reasoning-Distilled-GGUF) from Ollama...
docker compose exec ollama ollama pull kwangsuklee/Qwen3.5-4B-Claude-4.6-Opus-Reasoning-Distilled-GGUF
echo Done!
pause
