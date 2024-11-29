import time
import streamlit as st # type: ignore
import pandas as pd # type: ignore
import altair as alt # type: ignore


def statistics():
    """
    Displays statistical information and a visualization of the user's inputs.
    """
        
    st.title("Stats of your guesses!")

    # Guesses per category
    category_guesses = st.session_state.get("category_guesses", {})


    # Prepare data for visualization
    category_data = {
        "Category": [],
        "Guess Count": [],
        "Mean Guesses": [],
        "Games Played": [],

    }
    for category, guesses in category_guesses.items():
        if guesses:
            category_data["Category"].append(category)
            category_data["Guess Count"].append(sum(guesses))
            category_data["Mean Guesses"].append(
                sum(guesses) / len(guesses) if len(guesses) > 0 else 0
            )
            category_data["Games Played"].append(len(guesses))  # Add number of games played
    
    total_guesses = sum(len(guesses) for guesses in category_guesses.values() if guesses)
    mean_guesses = (sum(category_data["Guess Count"]) / total_guesses) if total_guesses > 0 else 0

    # Convert to DataFrame
    df_category = pd.DataFrame(category_data)

    # Find the category with the least mean guesses
    if not df_category.empty:  # Ensure DataFrame is not empty
        min_mean_index = df_category["Mean Guesses"].idxmin()
        least_guesses_category = df_category.loc[min_mean_index, "Category"]
        least_guesses_mean = df_category.loc[min_mean_index, "Mean Guesses"]

        # *** Display special highlight for the category with the least guesses ***
        st.markdown(
            f"""
            <div style="padding: 10px; background-color: #DFF2BF; border-radius: 10px; text-align: center;">
                <h3 style="color: #4F8A10;">Category with the least guesses:</h3>
                <p style="font-size: 20px; color: #4F8A10; font-weight: bold;">
                    {least_guesses_category} (Mean Guesses: {least_guesses_mean:.2f})
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Display mean of all guesses
    st.write(f"**Mean guesses: {mean_guesses:.2f}**") 

    # Display guesses per category as a table
    st.write(df_category)

    # Prepare data for a bar chart showing guesses per round
    round_data = {
        "Round": [],
        "Guesses": [],
        "Category": []
    }

    # Populate the data
    round_counter = 1
    for category, guesses in category_guesses.items():
        for guess_count in guesses:
            round_data["Round"].append(f"Round {round_counter}")
            round_data["Guesses"].append(guess_count)
            round_data["Category"].append(category)
            round_counter += 1

    # Convert to DataFrame
    df_rounds = pd.DataFrame(round_data)

    # Create a bar chart for guesses per round
    if not df_rounds.empty:
        bar_chart_rounds = alt.Chart(df_rounds).mark_bar().encode(
            x=alt.X("Round:N", title="Round"),
            y=alt.Y("Guesses:Q", title="Number of Guesses"),
            color=alt.Color("Category:N", title="Category"),
            tooltip=[alt.Tooltip("Round:N", title="Round"),
                    alt.Tooltip("Guesses:Q", title="Number of Guesses"),
                    alt.Tooltip("Category:N", title="Category")]
        ).properties(
            title="Guesses per round",
            width=600,
            height=400
        )

        # Display the chart
        st.altair_chart(bar_chart_rounds, use_container_width=True)

    # Create a DataFrame with a single value for total inputs count
        # Updated: Create a bar chart for the sum of the Guess Count column
    if not df_category.empty:
        df_total_guess_count = pd.DataFrame({
            'Metric': ['Sum of Guess Count'],  # Updated label
            'Value': [df_category["Guess Count"].sum()],  # Sum of the Guess Count column
        })

        # Updated: Bar chart visualization
        bar_chart = alt.Chart(df_total_guess_count).mark_bar(
            cornerRadiusTopLeft=10,
            cornerRadiusTopRight=10
        ).encode(
            x=alt.X('Metric:N', title='', axis=alt.Axis(labelAngle=0)),  # Use 'Metric' as x-axis
            y=alt.Y('Value:Q', title='Sum of Guesses ', scale=alt.Scale(domain=(0, df_total_guess_count["Value"].max() + 5))),
            tooltip=[alt.Tooltip('Value:Q', title="Sum of Guesses")]
        ).properties(
            title="Sum of guesses",
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
