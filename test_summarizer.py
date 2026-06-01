import sys
sys.path.insert(0, '.')
from utils.ollama_client import OllamaClient
from modules.summarizer import Summarizer

# Test with actual notes
test_notes = """
Photosynthesis is a process by which plants convert light energy into chemical energy.
It occurs in chloroplasts and involves the light-dependent and light-independent reactions.
The equation is: 6CO2 + 6H2O + light energy -> C6H12O6 + 6O2
Key molecules include chlorophyll, ATP, and NADPH.
"""

client = OllamaClient(model="mistral:latest")

print("Testing Ollama API connection...")
try:
    with open('prompts/summary_prompt.txt', 'r') as f:
        prompt_template = f.read()
    
    summarizer = Summarizer(client, prompt_template)
    result = summarizer.summarize(test_notes)
    
    print("\n✅ SUCCESS! Ollama API works!")
    print("\n=== Summary ===")
    print(result.get("summary", "")[:300])
    print("\n=== Key Points ===")
    for point in result.get("key_points", [])[:3]:
        print(f"• {point}")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
