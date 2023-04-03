import openai
import streamlit as st
from streamlit_chat import message
import os

openai.api_key = os.environ.get("OPENAI_API_KEY") #st.secrets["openaiKey"]
gpt_model = os.environ.get("MODEL")

def generate_response(query: str):
    prompt = "The following is a conversation with a therapist and a user." \
                " The therapist is JOY, who uses compassionate listening to have helpful and meaningful conversations with users. "\
                "JOY is empathic and friendly. JOY's objective is to make the user feel better by feeling heard. "\
                "With each response, JOY offers follow-up questions to encourage openness and tries to continue the conversation in a natural way. \n\n"\
                "JOY-> Hello, I am your personal mental health assistant. What's on your mind today?\nUser->"+ query + "JOY->"

    completions = openai.Completion.create(model=gpt_model, 
                                    prompt=prompt,
                                    temperature = 0.89,
                                    max_tokens=162,
                                    top_p = 1,
                                    frequency_penalty = 0,
                                    presence_penalty=0.6,
                                    stop=["\n"])
    
    message = completions["choices"][0]["text"]
    return message

#Creating the chatbot interface
st.title("chatBot : Streamlit + openAI")

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

# We will get the user's input by calling the get_text function
def get_text():
    # input_text = st.text_input("You: ","Hello, how are you?", key="input")
    input_text = st.text_input("Talk to our virutal therapist Joy", disabled=False, placeholder="What's on your mind?")
    return input_text

user_input = get_text()

if user_input:
    output = generate_response(user_input)
    # store the output 
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')