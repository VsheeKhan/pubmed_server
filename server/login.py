import streamlit as st
import json
import os
from langchain_community.tools.pubmed.tool import PubmedQueryRun
from langchain_community.document_loaders import PubMedLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import openai
from pyvis.network import Network
import networkx as nx
import re
import streamlit.components.v1 as components  # Import for displaying HTML in Streamlit

# File to store user credentials (username and password)
CREDENTIALS_FILE = "credentials.json"

# Function to load credentials from file
def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    return {}

# Function to verify credentials
def verify_credentials(username, password):
    credentials = load_credentials()
    return credentials.get(username) == password

# Function to handle login
def login():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if verify_credentials(username, password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.rerun()  # Trigger a rerun after successful login
        else:
            st.error("Invalid username or password")

# Function to handle logout
def logout():
    st.session_state["logged_in"] = False
    st.session_state.pop("username", None)
    st.rerun()  # Trigger a rerun after logout

# Main application logic
def main_app():
    st.set_page_config(page_title="Knowledge Graph Visualization", layout="wide")
    st.write(f"Welcome, {st.session_state['username']}!")

    # Input form for the query
    query = st.text_input("Enter your PubMed search query:", "")

    # Button to trigger the search and graph generation
    if st.button("Generate Knowledge Graph"):
        if query:
            # Perform PubMed search using the provided query
            loader = PubMedLoader(query)
            docs = loader.load()
            if len(docs) == 0:
                st.error("No documents found for the query.")
            else:
                context = "\n\n".join(doc.page_content for doc in docs)

                # Use OpenAI to generate the graph
                prompt_template = f"""Study the given context:\n{context}\nYou are a React developer who knows how to code React-vis-network-graph.\nBased on the context provided, create a network graph of the relationships and associations of elements in the context. Make sure every edge in the graph has a descriptive label.\nReturn the graph object with nodes and edges as a JSON object. You should not respond with anything except the graph JSON object."""
                
                # openai.api_key = "OPEN_AI_KEY"
                response = openai.ChatCompletion.create(
                    model="gpt-4-turbo",
                    messages=[{"role": "user", "content": prompt_template}]
                )
                response_text = response.choices[0].message['content']
                json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
                if json_match:
                    json_string = json_match.group(0)
                    try:
                        graph_data = json.loads(json_string)
                    except json.JSONDecodeError as e:
                        st.error(f"Failed to decode JSON: {e}")
                        return
                else:
                    st.error("No JSON found in the response.")
                    return

                # Create the network graph using the extracted graph data
                net = Network(height="750px", width="100%", notebook=False, directed=True)

                # Add nodes and edges from the parsed JSON
                for node in graph_data.get('nodes', []):
                    net.add_node(node['id'], label=node.get('label', ''), title=node.get('title', ''))

                for edge in graph_data.get('edges', []):
                    net.add_edge(edge['from'], edge['to'], title=edge.get('label', ''))

                # Generate the graph and save it as an HTML file
                output_path = "knowledge_graph.html"
                net.save_graph(output_path)

                # Display the HTML file in Streamlit
                with open(output_path, "r", encoding="utf-8") as f:
                    graph_html = f.read()

                components.html(graph_html, height=750, width=1200, scrolling=True)

                # Clean up the generated HTML file
                if os.path.exists(output_path):
                    os.remove(output_path)

        else:
            st.error("Please enter a query to search.")

    if st.button("Logout"):
        logout()

# Main function
def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"]:
        main_app()
    else:
        login()

if __name__ == "__main__":
    main()
