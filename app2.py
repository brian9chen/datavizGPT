import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

def run_UI():
    st.set_page_config(page_title="DataVizard", page_icon="🌟", layout="wide")
    st.title("DataVizard: Your Personal Data Dashboard")
    st.header("📊 Unlock Data Insights at Your Fingerprint 🧐")

    dataset_name = st.text_input("Enter the dataset name:")

    # default dataset
    iris = sns.load_dataset("iris")
    if dataset_name == "":
       dataset_name =  sns.load_dataset("iris")
    columns = dataset_name.columns.tolist()

    # Ask for user's need
    user_response = st.radio("Do you have a specific relationship of interest in mind already?", ("Yes", "No, take me to explore!"))

    if user_response == "Yes":
        variable_of_interest = st.multiselect("Select your variables of interest:", columns)
        visualize_button = st.button("Visualize Data")
        if visualize_button:
            
            if variable_of_interest:
                st.write(f"{variable_of_interest}")
            else:
                st.write("a graph generated from random variable of interest")
    else:
        user_question = st.text_input("Input the raw text here (dataset, var name)")
        st.write(f"a graph generated from random variable of interest generated from", {user_question})

if __name__ == "__main__":
    run_UI()
