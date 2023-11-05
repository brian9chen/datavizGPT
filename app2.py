import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import sys

def run_UI(code_str: str):
    print(code_str)
    st.set_page_config(page_title="DataVizard", page_icon="🌟", layout="wide")

    st.title("DataVizard: Your Personal Data Dashboard")
    st.header("📊 Unlock Data Insights at Your Fingerprint 🧐")

    # Load the environment variables (API keys)
    # load_dotenv()
    
    # initialize code
    code = '''def hello():
    print("Hello, Streamlit!")'''

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

    # Ask for user's need
    user_response = st.radio("Do you have a specific relationship of interest in mind already?", ("Yes", "No, take me to explore!"))

    if user_response == "Yes":
        variable_of_interest = st.multiselect("Select your variables of interest:", columns)
        ### PASS variable_of_interest to vectorstore
        # if variable_of_interest:
        # Call the function to generate the response
        # generate_response(user_need)
        visualize_button = st.button("Visualize Data")
        if visualize_button:
            st.write(f"Here's a graph based on your variable(s) of interest:, {variable_of_interest}")
            ### CODE FOR GRAPH ###
            user_need = st.radio("How do you like it so far?", ("Absolutely❤️Show me the code!", "Show me another graph 👀" ,"Not really😞I want..."))
            if user_need == "Absolutely❤️Show me the code!":    
                st.code(code, language='python')
            elif user_need == "Show me another graph 👀":
                # Add code to display another graph
                st.write("Here's another graph:")
                # ... (additional code for another graph)
            else:
                # Ask for user feedback
                user_feedback = st.text_input("No problem, tell me what you need!")
                st.write(f"A new graph generated based on your feedback: {user_feedback}")
                # ... (additional code based on user feedback)
    else:
        st.write("Here's a graph that you might find interesting:")
        ### CODE FOR GRAPH ###


    # Sidebar menu
    # with st.sidebar:
        # st.subheader("Dataset Uploader (optional)")
        # Document uploader
        # csv_files = st.file_uploader("Upload a public dataset you want to explore", type="csv", key="upload", accept_multiple_files=True)

if __name__ == "__main__":
    run_UI(code_str=sys.argv[1])