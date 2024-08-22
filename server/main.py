import streamlit as st
from langchain_community.tools.pubmed.tool import PubmedQueryRun
from langchain_community.document_loaders import PubMedLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import openai
from pyvis.network import Network
import networkx as nx
import os
import re
import json


# Streamlit app setup
st.set_page_config(page_title="Knowledge Graph Visualization", layout="wide")
st.title("PubMed Knowledge Graph Visualization")

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
            response_text = response.choices[0].message.content
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                json_string = json_match.group(0)
                try:
                    graph_data = json.loads(json_string)
                except json.JSONDecodeError as e:
                    print(f"Failed to decode JSON: {e}")
            else:
                print("No JSON found in the response.")

            # Create the network graph using the extracted graph data
            net = Network(height="750px", width="100%", notebook=False, directed=True)

            # Add nodes and edges from the parsed JSON
            for node in graph_data['nodes']:
                net.add_node(node['id'], label=node['label'], title=node.get('title', ""))

            for edge in graph_data['edges']:
                net.add_edge(edge['from'], edge['to'], title=edge.get('label', ""))

            # Generate the graph and save it as an HTML file
            output_path = "knowledge_graph.html"
            net.save_graph(output_path)

            # Display the HTML file in Streamlit
            with open(output_path, "r", encoding="utf-8") as f:
                graph_html = f.read()

            st.components.v1.html(graph_html, height=750, width=1200, scrolling=True)

            # Clean up the generated HTML file
            if os.path.exists(output_path):
                os.remove(output_path)

    else:
        st.error("Please enter a query to search.")
