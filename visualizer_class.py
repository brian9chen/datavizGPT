"""Functions to create prompt based on summarized data and user input."""

from typing import Dict, List, Optional
import pandas as pd

import easygui

class SecureVisualizer():
    """
    Attributes
        data: pandas DataFrame of original data set
        var_names: list of strings containing variable names to summarize
        notes: optional user-specified notes to include with API call
        prompt: string prompt to pass to OpenAI API; default set to "None"
        prompt_verified: boolean indicating whether user has validated prompt

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

    def create_prompt(self) -> None:
        """Format prompt for OpenAI API based on data summary and user inputs."""
        data_summary = self.summarize_data()
        notes = self.notes
        prompt = ""
        #TODO: create prompt based on data summary and user notes

        counter = 1
        
        for var in data_summary:
            type = var['type']
            
            if (type == "numeric"):
                stats = var['stats']
                
                size = stats['size']
                mean = stats['mean']
                sd = stats['sd']
                min = stats['min']
                max = stats['max']
            
                temp_prompt = "Variable #" + str(counter) + " is " + var + ". "
                temp_prompt = temp_prompt + "It consists of " + type + " data and it has " + str(size) + " datapoints. "
                temp_prompt = temp_prompt + "This variable has a mean of " + str(mean) + ", standard deviation of " + str(sd)
                temp_prompt = temp_prompt + ", mininum of " + str(min) + ", and a maximum of " + str(max) + ". "
                
            elif (type == "categorical"):
                stats = var['stats']
                size = stats['size']
                nunique = stats['nunique']
                
                temp_prompt = "Variable #" + str(counter) + " is " + var + ". "
                temp_prompt = temp_prompt + "There are " + str(nunique) + " categories, each with " + str(size) + " datapoints."
            
            prompt = prompt + temp_prompt
            counter = counter + 1
            
        prompt = prompt + "Please just print out the Python code (using the same variable names) to create the best visualization of these variables. "
        prompt = prompt + "Here are a few additional notes for guidance: " + notes
        
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

        # Determine variable types (require different statistics)
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
