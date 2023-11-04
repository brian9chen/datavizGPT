"""Main execution file for datavizGPT package."""

from typing import List, Optional

import pandas as pd

import easygui
import create_prompt; import send_prompt

def visualize(
    data: pd.DataFrame,
    vars: List[str],
    notes: Optional[str],
) -> None:
    """Visualize notional data (with similar data types and 
    statistical properties as original data) in Streamlit app.
    
    Args
        data: pandas DataFrame of original data set
        vars: list of variable names that user is interested in visualizing
        notes: optional notes to include to OpenAI API call
    
    Returns
        None
    """
    import pdb; pdb.set_trace()
    prompt = create_prompt.create_prompt(data=data, vars=vars, notes=notes)
    if create_prompt.user_verified_prompt:
        return "Success!"
        # Send prompt to OpenAI API here
    else:
        easygui.msgbox(
            msg='Prompt not validated--canceling.',
            title='Prompt canceled'
    )
        return None

if __name__ == "__main__":

    # Import example data set
    from ucimlrepo import fetch_ucirepo 
    data = fetch_ucirepo(id=890).data.original
    vars = ['time', 'oprior', 'symptom']

    import main
    result = main.visualize(
        data=data,
        vars=["time", "age", "symptom"],
        notes="The outcome variable is var2. Place var2 on the y-axis."
    )
    print(result)