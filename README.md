# Virtual Psychologist Streamlit Chat Application based on Fine Tuned ChatGPT

This Streamlit application allows users to have a conversation with a virtual psychologist powered by our fine tuned OpenAI ChatGPT model. Users can enter their message in the text input field and the ChatGPT model will generate a response. 

## Table of Contents

- [Virtual Psychologist Streamlit Chat Application based on Fine Tuned ChatGPT](#virtual-psychologist-streamlit-chat-application-based-on-fine-tuned-chatgpt)
  - [Table of Contents](#table-of-contents)
  - [Set up \& Installation](#set-up--installation)
    - [Fine tuning ChatGPT](#fine-tuning-chatgpt)
      - [Step 0: Install openai](#step-0-install-openai)
      - [Step 1: Preparing data for fine tuning](#step-1-preparing-data-for-fine-tuning)
      - [Step 2: Configuring data with Open AI api](#step-2-configuring-data-with-open-ai-api)
      - [Step 3: Fine tuning](#step-3-fine-tuning)
    - [Hosting the model with streamlit web app](#hosting-the-model-with-streamlit-web-app)
      - [Step 0: Install and create a virtual environment for the webapp with required dependencies](#step-0-install-and-create-a-virtual-environment-for-the-webapp-with-required-dependencies)
      - [Step 1: Kick start the stream lit app](#step-1-kick-start-the-stream-lit-app)

## Set up & Installation

### Fine tuning ChatGPT

Fine-tuning allows you to customize and optimize the performance of a pre-trained language model like GPT-3 to better suit any specific purposes. In our case, it is to provide free but professional psychotherapy service.

Benefits of fine-tuning:
* Improve the quality and relevance of its generated responses for our particular use case
* Higher accuracy and more natural-sounding language
* Token savings due to shorter prompts
* Lower latency requests

The full script is written in python and available at the jupyter notebook titled **'Prepare data and fine tune chatgpt with depression chat data.ipynb'**. Although it uses google drive throughout the process, it is no different to run on local environment. Key steps are summarised below:

#### Step 0: Install openai

Install Open ai python module in your environment:

```
pip install openai
```

#### Step 1: Preparing data for fine tuning

Open AI fine tuning api take additional training data in the following jsonl format:
```
[{'prompt' : '<user prompt text>', 'completion': '<ideal generated text>'}
{'prompt' : '<user prompt text>', 'completion': '<ideal generated text>'}
{'prompt' : '<user prompt text>', 'completion': '<ideal generated text>'}]
```

In this repo, we included this great handy dataset retrieved from Kaggle -- <u>__Depression Data for Chatbot__</u> [https://www.kaggle.com/datasets/narendrageek/mental-health-faq-for-chatbot]. As per the author, the data can be used to train the bot to help people suffering from depression, which is exactly our use case!

The data is stored in .yml format. The following python snippet is used to convert the raw data to Open AI desired format -- jsonl:

```
import json
import yaml

# load the raw data
with open('depression.yml', 'r') as file:
    data = yaml.safe_load(file)

# Extract the conversations
convos = data['conversations']

# Create prompt completion pairs
output = []

for convo in convos:
  completion = ''
  for i, dialog in enumerate(convo):
    if i == 0:
      prompt = dialog
      # p_encode = prompt.encode("ascii", "ignore")
      # prompt = p_encode.decode()
      prompt = prompt.replace("\xa0", " ")
      # print('prompt:',prompt)
    else:
      completion += " " + dialog
      # c_encode = completion.encode("ascii", "ignore")
      # completion = c_encode.decode()
      completion = completion.replace("\xa0", " ")
  completion = completion.strip()
  line = {'prompt': prompt, 'completion': completion}
  # print(line)
  output.append(line)

  print(output) /* [{'prompt': 'What Is Depression?', 'completion': 'Depression is a common and serious medical... */

# store the output in file named 'depression-d.jsonl'
with open('depression-d.jsonl', 'w') as outfile:
      for i in output:
          json.dump(i, outfile)
          outfile.write('\n')

```

#### Step 2: Configuring data with Open AI api

The data preparation is not done yet. The Open AI api comes with the 'prepare_data' module to ensure the data feeding to GPT model matches their develoment team requirement. We process the prompt-completion pair data again using the module:

```
!openai tools fine_tunes.prepare_data -f 'depression-d.jsonl'
```

It will return a file titled 'depression-d_prepared.jsonl' that conforms with fine tuning requirements.

#### Step 3: Fine tuning

Finally, we are ready to fine tune GPT-3 model for our purpose. 

```
!set OPENAI_API_KEY=<YOUR-API-KEY>
!openai api fine_tunes.create -t "depression-d_prepared.jsonl" -m davinci 
!openai api fine_tunes.follow -i ft-LKwrAVIKq6iFztZ6qffMbMpP
```

'fine_tunes.follow' api is used to get the fine tune job status on Open AI platform. When it is done, it will return the fine tuned model identifier and we can converse with it using 'completion.create' api.

Note that **davinci** is one of the gpt-3 base models (4 in total: Ada, Baggage, Currie, Davinvi). These base models are differentiated by speed and level of sophistication, with Ada being the fastest and Davinci being most sophisticated.

### Hosting the model with streamlit web app

#### Step 0: Install and create a virtual environment for the webapp with required dependencies

Streamlit is an open-source Python library that makes it easy to create and share beautiful, custom web apps for machine learning and data science. It is recommended to host any streamlit based app using virtualenv to prevent dependencies crash between python modules.

Install virtualenv with pip and create a virtual env called 'ChatBotApp'
```
pip install virtualenv
python3 -m venv ChatBotApp

source ChatBotApp/bin/activate # use the virtualenv

pip install streamlit
pip install streamlit_chat
pip install openai
```

#### Step 1: Kick start the stream lit app

All the code for the app is written in the file app/chatbot.py. For those who are interested, you can refer to the file for more details.

One thing I would like to highlight is the part where the app integrates with OpenAI.
```
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
```

The function is triggered when a user input a text stored as query in the program. To make the model response sounds like a psychologist, we provide the context and embed user's query in the prompt. Then the engineered prompt is passed to GPT model hosted on Open AI through the api with some specified parameters, and the response is returned.

Open AI api key and the model identifer are required to make this app run. Remember to input those info in the chatbot.py file. Kick start the app with the following snippet
```
streamlit run chatbot.py
```

The webapp will be host at <u>**localhost:8501**</u>. Go to the address via any browser and you can interact with the fine tuned chatbot.
