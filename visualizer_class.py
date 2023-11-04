"""Functions to create prompt based on summarized data and user input."""
import os
from typing import Dict, List, Optional

import pandas as pd

import easygui
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

class SecureVisualizer():
    """
    Attributes
        data: pandas DataFrame of original data set
        var_names: list of strings containing variable names to summarize
        notes: optional user-specified notes to include with API call
        prompt: string prompt to pass to OpenAI API; default set to "None"
        prompt_verified: boolean indicating whether user has validated prompt
        response: string response from OpenAI API; default set to "None"

    Methods
    
    """
    def __init__(
        self,
        data: pd.DataFrame,
        var_names: List[str],
        notes: Optional[str],
    ) -> None:
        "Sets class attributes"
        self.data = data
        self.var_names = var_names
        self.notes = notes
        self.prompt = "None"
        self.prompt_verified = False
        self.response = "None"

    def create_prompt(self) -> None:
        """Format prompt for OpenAI API based on data summary and user inputs."""
        data_summary = self.summarize_data()
        prompt = "Test"
        #TODO: create prompt based on data summary and user notes
        self.prompt = prompt

    def request_user_verification(self) -> None:
        """Validate with user that prompt should be passed to OpenAI API."""
        easygui.msgbox(
            msg='The prompt on the following screen will be passed to '+
            'OpenAI\'s Large Language Model API. You will have a chance on '+
            'the third screen to decide whether to cancel this prompt prior '+
            'to sending.', 
            title="Validate prompt"
        )
        easygui.msgbox(self.prompt, title="Validate prompt")
        self.prompt_verified = easygui.ynbox(
            msg='Would you like to send this prompt to ChatGPT/OpenAI?',
            title='Validate prompt',
            choices=('Yes', 'No'),
        )

    def send_prompt_and_get_response(self, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": self.prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0, # degree of randomness of the model's output
        )
        self.response = response.choices[0].message["content"]

    def launch_local_streamlit_app(self) -> None:
        """Launch Streamlit app on local server to visualize data."""
        pass

    def summarize_data(self) -> Dict:
        """Extract variable types and statistical properties of data.

        Returns
            dictionary of {var_names:{var_types, statistics}}
        """
        # Check that all variables exist in data
        if not all([var in self.data.columns for var in self.var_names]):
            raise ValueError(
                'One or more variable(s) not found in dataframe.'+
                'Please verify that variable names are spelled correctly.'
            )
            return
        # Separate variable types
        df_subset = self.data[self.vars]
        numeric_vars = df_subset.select_dtypes(include='numeric')
        categorical_vars = df_subset.select_dtypes(include='category')
        datetime_vars = df_subset.select_dtypes(include='datetime')
        # Extract variable summary
        vars_dict = {}
        for var in self.var_names:
            if var in numeric_vars:
                vars_dict[var] = {
                    'type':'numeric',
                    'stats':{
                        'size':self.data[var].count(),
                        'mean':self.data[var].mean(),
                        'sd':self.data[var].std(),
                        'min':self.data[var].min(),
                        'max':self.data[var].max(),
                    }
                }
            elif var in categorical_vars:
                vars_dict[var] = {
                    'type':'categorical',
                    'stats':{
                        'size':self.count(),
                        'nunique':self.data[var].nunique(),
                    }
                }
            elif var in datetime_vars:
                vars_dict[var] = {
                    'type':'datetime',
                    'stats':{
                        'size':self.count(),
                        'min':self.data[var].min(),
                        'max':self.data[var].max(),
                        'nunique':self.data[var].nunique(),
                    }
                }
            else:
                print(f'Variable "{var}" is not numeric, categorical, or '+
                      'datetime type and cannot currently be handled.')
                self.var_names = self.var_names.remove(var)
                continue

        return vars_dict
