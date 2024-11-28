import time
import streamlit as st # type: ignore
import pandas as pd # type: ignore
import altair as alt # type: ignore


def statistics():
        
    st.title("Stats of your guesses!")

    
    st.write("Last Inputs")
    st.write(st.session_state["inputs"])

    # Guesses per category
    #st.write("Guesses per category:")
    category_guesses = st.session_state.get("category_guesses", {})

    # Prepare data for visualization
    category_data = {
        "Category": [],
        "Guess Count": [],
        "Mean Guesses": [],

    }
    for category, guesses in category_guesses.items():
        print(guesses)
        if guesses:
            category_data["Category"].append(category)
            category_data["Guess Count"].append(sum(guesses))
            category_data["Mean Guesses"].append(
                sum(guesses) / len(guesses) if len(guesses) > 0 else 0
            )
    
    total_categories = len([c for c in category_guesses.values() if c])
    mean_guesses = sum(category_data["Guess Count"]) / total_categories if total_categories > 0 else 0

    st.write(f"Mean guesses: {mean_guesses:.2f}")

        


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

    # Display guesses per category as a table
    #st.write("Guesses per category (with means):")
    st.write(df_category)

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
