"""Visualizer class to generate OpenAPI prompt and call Streamlit app."""

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
        """Create prompt for OpenAI API based on data summary and user inputs."""
        data_summary = self.summarize_data()
        n_obs = self.data.shape[0]
        counter = 1
        for var_name, var_summary in data_summary.items():
            var_type = var_summary['type']
            var_stats = var_summary['stats']
            if (var_type == "numeric"):
                print(var_name, var_type, var_summary)
                prompt = f"""
                    Variable # {str(counter)} is {var_name}.
                    It consists of {var_type} data and has {n_obs} datapoints.
                    This variable's mean is {str(round(var_stats['mean'], 3))}.
                    Its standard deviation is {str(round(var_stats['sd']))}.
                    Its minimum value is {str(round(var_stats['min']))}.
                    Its maximum value is {str(round(var_stats['max']))}.
                """
            elif (var_type == "categorical"):
                prompt = f"""
                    Variable # {str(counter)} is {var_name}.
                    It consists of {var_type} data and has {n_obs} datapoints.
                    This variable's has {str(round(var_stats['nunique']))} unique categories.
                """
            elif (var_type == "datetime"):
                prompt = f"""
                    Variable # {str(counter)} is {var_name}.
                    It consists of {var_type} data and has {n_obs} datapoints.
                    This variable's minimum value is {str(round(var_stats['min']))}.
                    Its maximum value is {str(round(var_stats['max']))}. 
                    It has {str(round(var_stats['nunique']))} unique values.
                """
            counter = counter + 1
        # Add other notes to prompt
        prompt = f"""
            {prompt} Please only print out the Python code 
            (using the same variable names) to create the
            best or most creative visualization of these variables.
            Here are a few additional notes for guidance: {self.notes}
        """
        # Save prompt as attribute
        self.prompt = prompt
        print(prompt)

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
