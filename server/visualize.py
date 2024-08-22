import streamlit as st
from pyvis.network import Network
import networkx as nx
import os

# Streamlit app setup
st.set_page_config(page_title="Knowledge Graph Visualization", layout="wide")
st.title("Interactive Knowledge Graph")

# Define the graph data
graph_data = {
  "nodes": [
    {"id": "Psychobiotic", "label": "Psychobiotic", "title": "Bacteria with psychological benefits"},
    {"id": "Levilactobacillus brevis P30021", "label": "Levilactobacillus brevis P30021", "title": "Bacteria that produces GABA and acetylcholine"},
    {"id": "Lactiplantibacillus plantarum P30025", "label": "Lactiplantibacillus plantarum P30025", "title": "Bacteria that produces GABA and acetylcholine"},
    {"id": "Cognitive Performance", "label": "Cognitive Performance", "title": "Outcome measure of probiotic effect"},
    {"id": "GABA", "label": "GABA", "title": "Neurotransmitter"},
    {"id": "Acetylcholine", "label": "Acetylcholine", "title": "Neurotransmitter"},
    {"id": "Mood", "label": "Mood", "title": "Psychological outcome"},
    {"id": "Gut Microbiota", "label": "Gut Microbiota", "title": "Subjects' gut bacterial makeup"},
    {"id": "Palladium Nanoparticles", "label": "Palladium Nanoparticles", "title": "Catalyst in formic acid dehydrogenation"},
    {"id": "DUT-67-PZDC", "label": "DUT-67-PZDC", "title": "MOF used as support for Pd NPs"},
    {"id": "Formic Acid Dehydrogenation", "label": "Formic Acid Dehydrogenation", "title": "Chemical reaction catalyzed"},
    {"id": "H2 Production", "label": "Hydrogen Production", "title": "Resultant product of reaction"},
    {"id": "Airway Clearance Techniques", "label": "Airway Clearance Techniques", "title": "Techniques for managing bronchial secretions"},
    {"id": "Lung Volume Recruitment", "label": "Lung Volume Recruitment", "title": "Technique to increase lung/chest wall recruitment"},
    {"id": "Pediatric Patients", "label": "Pediatric Patients", "title": "Targeted population for ACT/LVR techniques"}
  ],
  "edges": [
    {"from": "Psychobiotic", "to": "Levilactobacillus brevis P30021", "label": "Includes"},
    {"from": "Psychobiotic", "to": "Lactiplantibacillus plantarum P30025", "label": "Includes"},
    {"from": "Levilactobacillus brevis P30021", "to": "GABA", "label": "Produces"},
    {"from": "Levilactobacillus brevis P30021", "to": "Acetylcholine", "label": "Produces"},
    {"from": "Lactiplantibacillus plantarum P30025", "to": "GABA", "label": "Produces"},
    {"from": "Lactiplantibacillus plantarum P30025", "to": "Acetylcholine", "label": "Produces"},
    {"from": "Levilactobacillus brevis P30021", "to": "Mood", "label": "Influences"},
    {"from": "Lactiplantibacillus plantarum P30025", "to": "Mood", "label": "Influences"},
    {"from": "Gut Microbiota", "to": "Mood", "label": "Influences"},
    {"from": "Gut Microbiota", "to": "Cognitive Performance", "label": "Related to"},
    {"from": "Mood", "to": "Cognitive Performance", "label": "Affects"},
    {"from": "Palladium Nanoparticles", "to": "DUT-67-PZDC", "label": "Supported by"},
    {"from": "Formic Acid Dehydrogenation", "to": "Palladium Nanoparticles", "label": "Catalyzed by"},
    {"from": "Formic Acid Dehydrogenation", "to": "H2 Production", "label": "Results in"},
    {"from": "Airway Clearance Techniques", "to": "Pediatric Patients", "label": "Applied to"},
    {"from": "Lung Volume Recruitment", "to": "Pediatric Patients", "label": "Applied to"}
  ]
}

# Create the network graph
net = Network(height="750px", width="100%", notebook=False, directed=True)

# Add nodes and edges from the data
for node in graph_data['nodes']:
    net.add_node(node['id'], label=node['label'], title=node.get('title', ""))

for edge in graph_data['edges']:
    net.add_edge(edge['from'], edge['to'], title=edge.get('title', ""))

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
