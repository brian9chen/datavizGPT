"""Visualizer class to generate OpenAPI prompt and call Streamlit app."""

import os
import textwrap
from typing import Dict, List, Optional

import pandas as pd

import easygui
import openai
openai.api_key = os.environ["OPENAI_API_KEY"]

from local_streamlit_class import LocalStreamlitApp

class SecureVisualizer():
    """
    Attributes
        data: pandas DataFrame of original data set
        var_names: list of strings containing variable names to summarize
        notes: optional user-specified notes to include with API call
        prompt: string prompt to pass to OpenAI API; default is empty string
        prompt_verified: boolean indicating whether user has validated prompt
        response: string response from OpenAI API; default is empty string

    Methods
    
    """
    def __init__(
        self,
        data: pd.DataFrame,
        var_names: List[str],
        notes: Optional[str],
    ) -> None:
        "Initialize class with attributes."
        self.data = data
        self.var_names = var_names
        self.notes = notes
        self.prompt = ""
        self.prompt_verified = False
        self.response = ""

    def create_prompt(self) -> None:
        """Create prompt for OpenAI API based on data summary and user inputs."""
        data_summary = self.summarize_data()
        n_obs = self.data.shape[0]
        counter = 1
        for var_name, var_summary in data_summary.items():
            var_prompt = ""
            var_type = var_summary['type']
            var_stats = var_summary['stats']
            if (var_type == "numeric"):
                var_prompt = textwrap.dedent(f"""
                    The name of variable # {str(counter)} is "{var_name}".
                    It consists of {var_type} data and has {n_obs} datapoints.
                    This variable's mean is {str(round(var_stats['mean'], 3))}.
                    Its standard deviation is {str(round(var_stats['sd']))}.
                    Its minimum value is {str(round(var_stats['min']))}.
                    Its maximum value is {str(round(var_stats['max']))}.
                """)
            elif (var_type == "categorical"):
                var_prompt = textwrap.dedent(f"""
                    The name of variable # {str(counter)} is "{var_name}".
                    It consists of {var_type} data and has {n_obs} datapoints.
                    This variable's has {str(round(var_stats['nunique']))} unique categories.
                """)
            elif (var_type == "datetime"):
                var_prompt = textwrap.dedent(f"""
                    The name of variable # {str(counter)} is "{var_name}".
                    It consists of {var_type} data and has {n_obs} datapoints.
                    This variable's minimum value is {str(round(var_stats['min']))}.
                    Its maximum value is {str(round(var_stats['max']))}. 
                    It has {str(round(var_stats['nunique']))} unique values.
                """)
            counter = counter + 1
            # Save variable prompt to full prompt attribute
            self.prompt += var_prompt
        # Add other notes to prompt
        self.prompt += textwrap.dedent(f"""
            Create three separate data visualizations that each include all of
            the variables in {self.var_names}. Return the Python code
            for each visualization as a separate text file.
            Use the original variable names in the code.
            Refer to the pandas DataFrame object in your code as "data".
            Adhere to the following guidelines enclosed in <> when creating 
            each of the three data visualizations:
            <{self.notes}>
        """) 

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
        app = LocalStreamlitApp(self.data, self.prompt, self.response)
        app.run_UI()
    
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
        df_subset = self.data[self.var_names]
        numeric_vars = df_subset.select_dtypes(include='number')
        categorical_vars = df_subset.select_dtypes(include='category')
        datetime_vars = df_subset.select_dtypes(include='datetime')
        # Extract variable summary
        vars_dict = {}
        for var in self.var_names:
            if var in numeric_vars:
                vars_dict[var] = {
                    'type':'numeric',
                    'stats':{
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
                        'nunique':self.data[var].nunique(),
                    }
                }
            elif var in datetime_vars:
                vars_dict[var] = {
                    'type':'datetime',
                    'stats':{
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
