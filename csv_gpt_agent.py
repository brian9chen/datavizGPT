#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# !pip install langchain
# !pip install tiktoken
get_ipython().system('pip install faiss-cpu')


# In[1]:


import os
import openai
from langchain import PromptTemplate
openai.api_key = os.environ["OPENAI_API_KEY"]
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType

from langchain_experimental.agents.agent_toolkits import create_csv_agent

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS


# In[2]:


from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.chains import ConversationalRetrievalChain
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.vectorstores import FAISS


# In[ ]:





# In[3]:


prompt = "you are an expert data visualisation analyst. The csv file you have been provided contains summary statistics of some dataset named xyz which is named as 'df' pandas dataframe. I want to create 3 visualizations for dataset xyz. Using the information provided by the summary statistics of xyz, give me a python code for most informative and asthetic visualizations"
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


# In[4]:


def get_chunks(text):
    """
    Function to get the chunks of text from the raw text

    Args:
        text (str): The raw text from the PDF file

    Returns:
        chunks (list): The list of chunks of text
    """

    # Initialize the text splitter
    splitter = CharacterTextSplitter(
        separator="\n", # Split the text by new line
        chunk_size=1000, # Split the text into chunks of 1000 characters
        chunk_overlap=200, # Overlap the chunks by 200 characters
        length_function=len # Use the length function to get the length of the text
    )

    # Get the chunks of text
    chunks = splitter.split_text(text)

    return chunks

def get_vectorstore(chunks):
    """
    Function to create avector store for the chunks of text to store the embeddings

    Args:
        chunks (list): The list of chunks of text

    Returns:
        vector_store (FAISS): The vector store for the chunks of text
    """

    # Initialize the embeddings model to get the embeddings for the chunks of text
    embeddings = OpenAIEmbeddings()

    # Create a vector store for the chunks of text embeddings
    # Can use any other online vector store (Elasticsearch, PineCone, etc.)
    vector_store = FAISS.from_texts(texts=chunks, embedding=embeddings)

    return vector_store



text = """
Test vector store
"""
vector_store = get_vectorstore(text)


# In[6]:


llm = ChatOpenAI(model_name='gpt-3.5-turbo-16k', temperature=0.1)

# Initialize the chat memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create a conversation chain for the chat model
conversation_chain = ConversationalRetrievalChain.from_llm(
    llm=llm, # Chat model
    retriever=vector_store.as_retriever(), # Vector store
    memory=memory, # Chat memory
)


# In[ ]:


# prefix = """You are an experienced analyst"""
# suffix = """{chat_history}

# {prompt}"""

# prompt = ZeroShotAgent.create_prompt(
#     [],
#     prefix=prefix,
#     suffix=suffix,
#     input_variables=["chat_history", "prompt"],
# )

# agent = create_csv_agent(
#     ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k"),
#     "describe_data.csv",
#     verbose=True,
#     agent_type=AgentType.OPENAI_FUNCTIONS, 
#     memory=memory
# )

# agent_chain = AgentExecutor.from_agent_and_tools(
#     agent=agent, verbose=True, memory=memory, tools=[]
# )


# In[7]:


agent = create_csv_agent(
    llm,
    "describe_data.csv",
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS, 
    memory=memory
)


# In[ ]:





# In[17]:


x = agent.run(prompt)


# In[19]:


print(x)


# In[10]:


response1= str(agent.run(prompt))


# In[11]:


response1


# In[12]:


feedback = "Add a black background to the visualizations"


# In[13]:


follow_up = f"""
Following is a piece of python code for visualizations: ```
{response1}
```

Your job is to improve these visua;izations based on the following feedback - ```{feedback} ```
"""


# In[14]:


follow_up


# In[15]:


response = conversation_chain({'question': follow_up})


# In[21]:


response


# In[22]:


print(response["answer"])


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




