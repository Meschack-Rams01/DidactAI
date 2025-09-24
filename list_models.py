import google.generativeai as genai

# Configure the API key
api_key = "AIzaSyCiUzGh5rm96bh-Kqce4S-yRj_yq3U1O_A"
genai.configure(api_key=api_key)

print("Available Gemini models:")
print("-" * 40)

try:
    models = genai.list_models()
    for model in models:
        print(f"Model: {model.name}")
        print(f"  Supported methods: {model.supported_generation_methods}")
        print(f"  Description: {model.description}")
        print("-" * 40)
except Exception as e:
    print(f"Error listing models: {e}")