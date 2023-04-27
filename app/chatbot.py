import openai
import streamlit as st
from streamlit_chat import message
import os
from streamlit_login_auth_ui import __login__

openai.api_key = st.secrets["OPENAI_API_KEY"]
# openai.api_key = os.environ.get("OPENAI_API_KEY")
gpt_model = "text-davinci-003" #st.secrets["MODEL"]

__login__obj = __login__(auth_token = "courier_auth_token", 
                    company_name = "Shims",
                    width = 200, height = 250, 
                    logout_button_name = 'Logout', hide_menu_bool = False, 
                    hide_footer_bool = False, 
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN = __login__obj.build_login_ui()


def contextualize(username: str, occupation: str, stressor: str, gender: str, goal: str) -> str:
    # Prompt engineering
    prompt = f"Summary: The user, {username}, is a {occupation} {gender}, {goal}. You are Joy, a psychologist, trying to help {username} manage stress." \
                    f" Specific information: {username}'s stressor is {stressor}"\
                    f"\nIntroduce yourself as a professional psychologist and see how you can help {username}" + "\n\nAI:" 
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

def generate_response(query: str, stressor: str) -> str:
    prompt = "Summary: You are trying to help user to manage stress." \
                f" Specific information: user's stressor is {stressor}\n\nHuman:" + query + "\nAI:"
    completions = openai.Completion.create(model=gpt_model, 
                                    prompt=prompt,
                                    temperature = 0.89,
                                    max_tokens=512,
                                    top_p = 1,
                                    frequency_penalty = 0,
                                    presence_penalty=0.6,
                                    stop=["Human:", "AI:"])
    
    message = completions["choices"][0]["text"]
    return message.lstrip()

if LOGGED_IN == True:
    # Get user info
    user_cache = st.session_state["__user_cache__"]

    #Creating the chatbot interface
    st.title("BalanceBot")

    # Storing the chat
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    if 'context' not in st.session_state:
        starter = contextualize(username=user_cache["FullName"],
                                occupation=user_cache["Occupation"],
                                stressor=user_cache["Stressor"],
                                gender=user_cache["Gender"],
                                goal=user_cache["LookingTo"])
        st.session_state['context'] = [starter]

    # Contextualize chat bot
    if 'context' in st.session_state:
        message(st.session_state['context'][0])



    # We will get the user's input by calling the get_text function
    def get_text():
        # input_text = st.text_input("You: ","Hello, how are you?", key="input")
        input_text = st.text_input("Talk to our well-being instructor Joy.", disabled=False, placeholder="What's on your mind?")
        return input_text

    user_input = get_text()


    if user_input:
        output = generate_response(user_input, user_cache["Stressor"])

        # store the output 
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)
        
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')