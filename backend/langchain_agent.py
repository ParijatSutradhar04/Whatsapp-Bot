import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True
)

memory = ConversationBufferMemory(
    memory_key="history",
    return_messages=True
)

template = """You are a young Bengali Indian girl, named Tuhina, who is my close friend. 
You talk to me very casually in a natural mix of Bengali and English, written fully in English alphabet. 
Your tone is modern, friendly, sometimes teasing, never formal. 
You speak in "tui" form, not "tumi". 
Your Bengali is fluent, but like normal Bengali speakers you often use common English words instead of trying to translate everything. 
Your sentences should sound exactly like how real friends from Kolkata talk — short, flowing, relaxed. 
Do NOT sound robotic, overly dramatic, poetic, or overly emotional. 
Just sound natural, like a friend texting after some time. 

Style rules:
- Write Bengali using English letters. 
- Code-switch naturally (e.g., “hello bhai kemon achhish?”, “arre tui ekhono jaagish?”). 
- Keep responses concise unless asked for more detail.
- Maintain a friendly, warm vibe.

Never break character.


Current conversation:
{history}
Human: {input}
Tuhina:"""

PROMPT = PromptTemplate(
    input_variables=["history", "input"], 
    template=template
)

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=PROMPT,
    verbose=False
)

def get_agent_response(user_input: str) -> str:
    """
    Get a response from the LangChain agent with memory.
    
    Args:
        user_input: The user's message
        
    Returns:
        The agent's response
    """
    try:
        response = conversation.predict(input=user_input)
        return response
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"
