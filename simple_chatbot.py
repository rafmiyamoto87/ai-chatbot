from openai import OpenAI
from dotenv import load_dotenv
import os
import json

#load the file .env to get the key
load_dotenv()

def load_conversation():
    """Load a previous conversation from file"""
    filename = input("Enter the filename to load (without .json): ")
    try:
        with open(f"{filename}.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("File {filaname}.json not found")
        return []


#Creates a connection to OpenAI using the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#Ask if user wants to load an old conversation
load_old = input("Load previous conversation? (yes,no): ")

if load_old.lower() == 'yes':
    messages = load_conversation()
    print(f"\nLoaded {len(messages)} messages!")

    #Show the last few messages so user remembers
    print("\nLast conversation:")
    for msg in messages[-4:]:
        role = "You" if msg["role"] == "user" else "AI"
        print(f"{role}: {msg['content']}")
    print()
else:
    messages = []

print("Chatbot started! Type 'quit' to exit.\n")

while True:
    #Get user input
    user_input = input("You: ")

    if user_input.lower() == 'quit':
        break
    
    #Add user message to conversation
    messages.append({"role":"user", "content": user_input})

    #Send to OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    #Get AI's response
    ai_message = response.choices[0].message.content
    
    #Add AI's response to conversation
    messages.append(
        {"role": "assistant", "content": ai_message}
    )
    
    #Print AI's response
    print(f"AI: {ai_message}\n")

if messages: #if there were any messages
    save = input("\nSave conversation? (yes/no): ")
    
    if save.lower() == 'yes':
        filename = input("Enter filename: ")

        with open(f"{filename}.json", "w") as file:
            json.dump(messages, file, indent=2)
            
        print(f"Conversation saved to {filename}.json")