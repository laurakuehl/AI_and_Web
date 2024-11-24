import time
import streamlit as st
import pandas as pd
import altair as alt

def statistics():
        
    st.title("Statistik über deine Eingaben")

    total_inputs = len(st.session_state["inputs"])
    unique_inputs = len(set(st.session_state["inputs"]))

    st.write(f"Anzahl der Eingaben: {total_inputs}")
    st.write(f"Anzahl der einzigartigen Eingaben: {unique_inputs}")

    st.write("Alle gespeicherten Eingaben:")
    st.write(st.session_state["inputs"])

    # Guesses per category
    st.write("Guesses per category:")
    category_guesses = st.session_state.get("category_guesses", {})

    # Prepare data for visualization
    category_data = {
        "Category": [],
        "Guess Count": [],
    }
    for category, guesses in category_guesses.items():
        category_data["Category"].append(category)
        category_data["Guess Count"].append(len(guesses))

    # Convert to DataFrame
    df_category = pd.DataFrame(category_data)

    # Display guesses per category as a table
    st.write(df_category)

    # Create a DataFrame with a single value for total inputs count
    df_total_inputs = pd.DataFrame({
        'Category': ['Total Inputs'],
        'Count': [total_inputs]
    })

    # Create a fancy bar chart with Altair
    bar_chart = alt.Chart(df_total_inputs).mark_bar(
        cornerRadiusTopLeft=10,
        cornerRadiusTopRight=10
    ).encode(
        x=alt.X('Category:N', title='', axis=alt.Axis(labelAngle=0)),  # Nominal type for Category
        y=alt.Y('Count:Q', title='Total Number of Inputs', scale=alt.Scale(domain=(0, total_inputs + 5))),
        tooltip=[alt.Tooltip('Count:Q', title="Total Inputs")]
    ).properties(
        width=400,
        height=300
    ).configure_mark(
        color=alt.Gradient(
            gradient="linear",
            stops=[               
                alt.GradientStop(color="#FF0000", offset=0),    # Red
                alt.GradientStop(color="#FF7F00", offset=0.16), # Orange
                alt.GradientStop(color="#FFFF00", offset=0.33), # Yellow
                alt.GradientStop(color="#00FF00", offset=0.5),  # Green
                alt.GradientStop(color="#0000FF", offset=0.66), # Blue
                alt.GradientStop(color="#4B0082", offset=0.83), # Indigo
                alt.GradientStop(color="#8B00FF", offset=1)     # Violet
],
            x1=1, x2=1, y1=1, y2=0
        )
    ).configure_view(
        strokeWidth=0  # Remove outer border around chart
    )
    st.altair_chart(bar_chart, use_container_width=True)

