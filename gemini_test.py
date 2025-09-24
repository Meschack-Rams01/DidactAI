import google.generativeai as genai
import os

def test_gemini():
    # Configure the API key
    api_key = "AIzaSyCiUzGh5rm96bh-Kqce4S-yRj_yq3U1O_A"
    genai.configure(api_key=api_key)
    
    # Initialize the model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    print("🤖 Gemini AI Test Started!")
    print("-" * 50)
    
    try:
        # Test basic chat
        response = model.generate_content("Hello! Can you tell me a fun fact about Python programming?")
        print("✅ Connection successful!")
        print(f"Gemini says: {response.text}")
        print("-" * 50)
        
        # Interactive chat loop
        print("You can now chat with Gemini! Type 'quit' or 'exit' to stop.\n")
        
        while True:
            user_input = input("You: ")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if user_input.strip() == "":
                continue
                
            try:
                response = model.generate_content(user_input)
                print(f"Gemini: {response.text}\n")
            except Exception as e:
                print(f"❌ Error generating response: {e}\n")
                
    except Exception as e:
        print(f"❌ Error connecting to Gemini: {e}")
        print("Please check your API key and internet connection.")

if __name__ == "__main__":
    test_gemini()