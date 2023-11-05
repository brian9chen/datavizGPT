import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import random
import inspect
#from streamlit_pandas_profiling import st_profile_report
#from langchain.embeddings import OpenAIEmbeddings
#from langchain.vectorstores import FAISS
#from langchain.chat_models import ChatOpenAI
#from langchain.memory import ConversationBufferMemory
#from langchain.chains import ConversationalRetrievalChain
#from html_chatbot_template import css, bot_template, user_template

def run_UI():
    st.set_page_config(page_title="DataVizard", page_icon="🌟", layout="wide")
    st.title("DataVizard: Your Personal Data Dashboard")
    st.header("📊 Unlock Data Insights at Your Fingerprint with LLM 🧐")

    # Load the environment variables (API keys)
    # load_dotenv()
    
    # initialize code
    code = '''def hello():
    print("Hello, Streamlit!")'''

    # Initialize plot code
    def generate_scatter_plot(x_variable, y_variable=None):
        if y_variable is None:
            sns.histplot(data=iris, x=x_variable)
            plt.title(f"Scatter Plot of {x_variable}")
        else:
            sns.scatterplot(data=iris, x=x_variable, y=y_variable)
            plt.xlabel(x_variable)
            plt.ylabel(y_variable)
            plt.title(f"Scatter Plot of {x_variable} vs {y_variable}")

        return plt

    tab1, tab2 = st.tabs([
    "🛡️ Private Mode: Let's visualize on a demo",
    "🚀 Public Mode: Upload the dataset and see real relationship"
])
    with tab1:
        dataset_name = ""
        # default dataset
        iris = sns.load_dataset("iris")
        if dataset_name == "":
            dataset_name =  sns.load_dataset("iris")
            columns = dataset_name.columns.tolist()

    with tab2:
        st.write("Dataset Uploader")
        # Document uploader
        dataset_name = st.file_uploader("Upload a public dataset you want to explore", type="csv", key="upload", accept_multiple_files=True) 
    
    # An initial look of data
    # pr = dataset_name.profile_report()
    # st_profile_report(pr)
        
    # Ask for user's need
    user_response = st.radio("Do you have a specific relationship of interest in mind already?", ("Yes", "No, take me to explore!"))
    if user_response == "Yes":
        variable_of_interest = st.multiselect("Select your variable(s) of interest:", columns)
        st.write(f"Your variable(s) of interest:, {variable_of_interest}")
        ### PASS variable_of_interest to vectorstore
        # if variable_of_interest:
        # Call the function to generate the response
        # generate_response(user_need)
        st.button("Reset", type="primary")
        if st.button("Go"):
            if len(variable_of_interest) == 1:
                x_variable = variable_of_interest[0]
                figure = generate_scatter_plot(x_variable)
                st.pyplot(figure)
            elif len(variable_of_interest) == 2:
                x_variable, y_variable = variable_of_interest
                figure = generate_scatter_plot(x_variable, y_variable)
                st.pyplot(figure)
            else:
                x_variable, y_variable = random.sample(variable_of_interest, 2)
                figure = generate_scatter_plot(x_variable, y_variable)
                st.pyplot(figure)

        else:
            st.write("Here's a graph that might interest you")
        user_need = st.radio("How do you like it so far?", ["Absolutely ❤️ Show me the code!", "Vary it a little bit 👀", "Not really 😞 I want..."], index=0)
        if user_need == "Absolutely ❤️ Show me the code!":    
            # code = generate_scatter_plot.__code__
            code = inspect.getsource(generate_scatter_plot)
            st.code(code, language='python')
        elif user_need == "Vary it a little bit 👀":
            # Add code to display another graph
            st.write("Here's a variation of previous graph:")
            if len(variable_of_interest) == 1:
                x_variable = variable_of_interest[0]
                figure = generate_scatter_plot(x_variable)
                st.pyplot(figure)
            elif len(variable_of_interest) == 2:
                x_variable, y_variable = variable_of_interest
                figure = generate_scatter_plot(x_variable, y_variable)
                st.pyplot(figure)
            else:
                x_variable, y_variable = random.sample(variable_of_interest, 2)
                figure = generate_scatter_plot(x_variable, y_variable)
                st.pyplot(figure)
        else:
            # Ask for user feedback
            user_feedback = st.text_input("No problem, tell me what you need!")
            st.write(f"A new graph generated based on your feedback: {user_feedback}")

    # Sidebar menu
    # with st.sidebar:
        # st.subheader("Dataset Uploader (optional)")
        # Document uploader
        # csv_files = st.file_uploader("Upload a public dataset you want to explore", type="csv", key="upload", accept_multiple_files=True)

if __name__ == "__main__":
    run_UI()
