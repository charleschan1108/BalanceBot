import openai
import streamlit as st
from streamlit_chat import message
import os

openai.api_key = st.secrets["OPENAI_API_KEY"]
gpt_model = "text-davinci-003" #st.secrets["MODEL"]

def contextualize():
    # Prompt engineering
    prompt = "Summary: The user, Sonal, is a working professional, looking to form good habits. You are Joy, a psychologist, trying to help Sonal manage stress." \
                    " Specific information: Sonal's stressor is work"\
                    "\nIntroduce yourself as a professional psychologist" + "\n\nAI:" 
    completions = openai.Completion.create(model=gpt_model, 
                                        prompt=prompt,
                                        temperature = 0.89,
                                        max_tokens=256,
                                        top_p = 1,
                                        frequency_penalty = 0,
                                        presence_penalty=0.6,
                                        stop=["Human:", "AI:"])
    
    message = completions["choices"][0]["text"]
    return message.lstrip()

def generate_response(query: str):
    prompt = "Summary: You are trying to help user to manage stress." \
                " Specific information: user's stressor is work\n\nHuman:" + query + "\nAI:"
    completions = openai.Completion.create(model=gpt_model, 
                                    prompt=prompt,
                                    temperature = 0.89,
                                    max_tokens=256,
                                    top_p = 1,
                                    frequency_penalty = 0,
                                    presence_penalty=0.6,
                                    stop=["Human:", "AI:"])
    
    message = completions["choices"][0]["text"]
    return message.lstrip()

#Creating the chatbot interface
st.title("chatBot : Streamlit + openAI")

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'context' not in st.session_state:
    starter = contextualize()
    st.session_state['context'] = [starter]

# Contextualize chat bot
if st.session_state['context']:
    message(st.session_state['context'][0])



# We will get the user's input by calling the get_text function
def get_text():
    # input_text = st.text_input("You: ","Hello, how are you?", key="input")
    input_text = st.text_input("Talk to our virtual psychologist Joy.", disabled=False, placeholder="What's on your mind?")
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