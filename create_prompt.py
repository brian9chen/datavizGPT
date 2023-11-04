"""Create prompt summarizing data and save locally for user review."""

from typing import Dict, List, Optional
import pandas as pd
import easygui

def user_verified_prompt(prompt: str) -> bool:
    """Validate with user that prompt should be passed to OpenAI API.
    
    Args
        prompt: full prompt string to pass to OpenAI API
    
    Returns
        boolean indicating True if prompt confirmed as valid, False otherwise
    """
    easygui.msgbox(
        msg='The prompt on the following screen will be passed to OpenAI\'s Large Language '+
        'Model API. You will have a chance on the third screen to decide whether to '+
        'cancel this prompt prior to sending.', 
        title="Validate prompt"
    )
    easygui.msgbox(prompt, title="Validate prompt")
    user_verified_bool = easygui.ynbox(
        msg='Would you like to send this prompt to ChatGPT/OpenAI?',
        title='Validate prompt',
        choices=('Yes', 'No'),
    )
    return user_verified_bool


def create_prompt(
    data: pd.DataFrame,
    vars: List[str],
    notes: Optional[str],
) -> str:
    """Format prompt for OpenAI API based on data summary and user inputs.
    
    Args
        data: pandas DataFrame
        vars: list of strings containing variable names to summarize
        notes: optional user-specified notes to include with API call
    
    Returns
        prompt string for OpenAI API
    """
    data_summary = summarize_data(data=data, vars=vars)
    prompt = "Test"
    #TODO: create prompt based on data summary and user notes
    return prompt


def summarize_data(data: pd.DataFrame, vars: List[str]) -> Dict:
    """Extract variable types and statistical properties of data.
    
    Args
        data: pandas DataFrame
        vars: list of strings containing variable names to summarize
    
    Returns
        dictionary of {var_names:{var_types, statistics}}

    """
    if not all([var in data.columns for var in vars]):
        raise ValueError(
            'One or more variable(s) not found in dataframe.'+
            'Please verify that variable names are spelled correctly.'
        )
    vars_dict = {}
    for var in vars:
        vars_dict[var] = {
            'type':str(data[var].dtype),
            'stats':{
                'mean':data[var].mean(),
                'sd':data[var].std(),
                'min':data[var].min(),
                'max':data[var].max(),
            }
        }
    return vars_dict
