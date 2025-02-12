import streamlit as st
import requests
import pandas as pd

st.title("🔍 Generate SEO Keywords")

if "product_title" in st.session_state and st.session_state.product_title:
    st.subheader(f"Generating SEO Keywords for: {st.session_state.product_title}")

    def generate_keywords(title):
        """Call FastAPI backend to generate keywords"""
        response = requests.post(
            "http://localhost:8001/keywords/generate",
            json={"title": title}
        )
        if response.status_code == 200:
            return response.json()
        return {}

    if st.button("🔑 Generate Keywords"):
        data = generate_keywords(st.session_state.product_title)
        
        if "keywords" in data:
            st.session_state.generated_keywords = ", ".join(data["keywords"])
            st.success(f"✅ Keywords: {st.session_state.generated_keywords}")

        if "interest_over_time" in data:
            st.subheader("📊 Interest Over Time")
            timeline_data = data["interest_over_time"].get("timeline_data", [])

            if timeline_data:
                # Extract dates and format data
                dates = [entry["date"] for entry in timeline_data]
                df = pd.DataFrame(index=dates)

                for entry in timeline_data:
                    for value in entry["values"]:
                        query = value["query"]
                        extracted_value = value["extracted_value"]
                        if query not in df:
                            df[query] = None
                        df.at[entry["date"], query] = extracted_value

                #  Plot the graph
                st.line_chart(df)
            else:
                st.warning("⚠️ No trend data available.")

else:
    st.warning("⚠️ Please enter a product title and upload an image on the Home page first.")
