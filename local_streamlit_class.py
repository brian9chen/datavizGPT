"""Class to launch Streamlit app on local server"""

import os
import re
import subprocess
from typing import Dict, List, Optional
import webbrowser

import pandas as pd

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

    def run_UI(self) -> None:
        parsed_response = self.parse_response()
        command = ["streamlit", "run", "app2.py", f"-- {parsed_response}"]
        process = subprocess.Popen(command, shell=True)
        webbrowser.open_new_tab("http://localhost:8501") #TODO: figure out how to set port

    def parse_response(self) -> List[str]:
        """Parse OpenAI API response to extract code for visualization."""
        return [re.split("visualization\n", self.response)[-1]]
        
        
        
        
        
        
        
        