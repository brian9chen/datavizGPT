"""Class to launch local Streamlit app"""

import os
import textwrap
from typing import Dict, List, Optional

import pandas as pd

import easygui
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

class LocalStreamlitApp:
    """
    
    Attributes
        data: pandas DataFrame of original data set
        prompt: string prompt passed to OpenAI API
        response: string response from OpenAI API

    Methods
    
    """
    
    def __init__(
        self,
        data: pd.DataFrame,
        prompt: str,
        response: str,
    ) -> None:
        "Initialize class with attributes."
        self.data = data
        self.prompt = prompt
        self.response = response

    def run(self) -> None:
        pass
        
        
        
        
        