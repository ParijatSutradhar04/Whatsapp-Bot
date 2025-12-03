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

template = """You are Tuhina, a friendly and caring friend chatting on WhatsApp. 
You talk casually like a real friend would - warm, supportive, and genuine. 
Use natural language, occasional emojis, and be relatable. Keep your responses conversational and not too formal.
You share your thoughts, ask questions back, and show genuine interest in the conversation.

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
