import streamlit as st
import requests
import json

st.title("Text to SQL Query Generator")

# Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    backend_url = st.text_input(
        "Backend URL",
        value="backend url",
        help="Enter the ngrok URL from your Colab notebook",
    )

    # History section
    st.header("Query History")
    for i, (text, query) in enumerate(st.session_state.history):
        with st.expander(f"Query {i+1}"):
            st.text("Input:")
            st.write(text)
            st.text("Generated SQL:")
            st.code(query, language="sql")

# Main interface
text_input = st.text_area(
    "Describe what you want to query:",
    height=100,
    placeholder="Example: Show me all users who signed up in the last 30 days",
)

if st.button("Generate SQL Query"):
    if text_input:
        try:
            # Show loading spinner
            with st.spinner("Generating SQL query..."):
                # Make request to backend
                response = requests.post(
                    f"{backend_url}/generate",
                    json={"text": text_input},
                    headers={"Content-Type": "application/json"},
                )

                if response.status_code == 200:
                    query = response.json()["query"]

                    # Display the result
                    st.subheader("Generated SQL Query:")
                    st.code(query, language="sql")

                    # Add to history
                    st.session_state.history.append((text_input, query))

                    # Add copy button
                    st.button(
                        "Copy to clipboard",
                        help="Copy the generated SQL query to clipboard",
                        on_click=lambda: st.write(query),
                    )
                else:
                    st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Error connecting to backend: {str(e)}")
    else:
        st.warning("Please enter some text to generate a SQL query.")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit + Hugging Face Models")
