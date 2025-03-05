# chatbot/chat_logic.py

RESPONSES = {
    "hello": "Hello! Welcome to XYZ Real Estate. How can I assist you today?",
    "hi": "Hi there! How can I help you?",
    "properties": "We have properties in Downtown, Suburbs, and Beachfront areas. Which are you interested in?",
    "price": "Our properties range from $200,000 to $1.5M. What’s your budget?",
    "schedule visit": "Sure! Please provide your name and preferred date for a visit.",
    "contact": "You can reach us at contact@xyzestate.com or call +1-800-123-4567.",
    "default": "I’m sorry, I didn’t understand that. Could you rephrase or ask about properties, prices, or scheduling a visit?"
}

def get_chatbot_response(user_input):
    user_input = user_input.lower().strip()
    
    # Check for keywords in user input
    if "hello" in user_input or "hi" in user_input:
        return RESPONSES["hello"]
    elif "property" in user_input or "house" in user_input:
        return RESPONSES["properties"]
    elif "price" in user_input or "cost" in user_input:
        return RESPONSES["price"]
    elif "schedule" in user_input or "visit" in user_input:
        return RESPONSES["schedule visit"]
    elif "contact" in user_input or "email" in user_input:
        return RESPONSES["contact"]
    else:
        return RESPONSES["default"]