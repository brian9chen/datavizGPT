"""Main execution file for datavizGPT package."""

from typing import List, Optional

import pandas as pd
import easygui

from visualizer_class import SecureVisualizer

def visualize(
    data: pd.DataFrame,
    var_names: List[str],
    notes: Optional[str],
) -> None:
    """Visualize 
    
    Args
        data: pandas DataFrame of original data set
        var_names: list of variable names that user is interested in visualizing
        notes: optional notes to include to OpenAI API call
    
    Returns
        None
    """
    # Instantiate visualizer class
    visualizer = SecureVisualizer(data, var_names, notes)
    visualizer.create_prompt()
    visualizer.request_user_verification()
    if visualizer.prompt_verified:
        visualizer.send_prompt_and_get_response()
        # visualizer.launch_local_streamlit_app()
        return visualizer.response

    else:
        easygui.msgbox(
            msg='Canceling prompt (no information was sent).',
            title='Prompt canceled'
        )
        return "Canceled"

if __name__ == "__main__":

    # Import example data set
    from ucimlrepo import fetch_ucirepo 
    data = fetch_ucirepo(id=890).data.original
    var_names = ['time', 'age', 'symptom']

    result = visualize(
        data=data,
        var_names=var_names,
        notes="The outcome variable is 'symptom'. Place 'symptom' on the y-axis."
    )
    print(result)