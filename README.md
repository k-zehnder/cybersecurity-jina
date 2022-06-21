# Cybersecurity Dashboard Made with Jina and Streamlit

This repo is a work in progress :)

What is this?
This project uses the Jina Ecosystem and Streamlit to build a "network intrusion" detector that simulates monitoring network traffic in real-time. It is heavily inspired by a notebook I found [over on Pinecone](https://www.pinecone.io/docs/examples/it-threat-detection/).  

The goal of this project is to demonstrate how you can get far better results (precision/recall) on a classification task using similarity search with DocumentArray than you get just using the neural network itself.

In other words, when I "chopped off" the classification layer, used the network as a feature extractor and stored the embeddings data in a DocumentArray, the subsequent precision/recall using similarity search with DocumentArray was significantly better than just taking the results of the neural network itself. It shows the power behind using similarity search as a basis for classification. 

I like this project because I think it showcases some of the power and flexibility Jina offers (e.g., parallel indexing of documents to independent document stores using complex flow topologies, visualizing embeddings with the embeddings projector, ease of scale, etc..). Jina can handle far more interesting and demanding challenges than simply what goes into a search box. I believe this project demonstrates that.

![wip](data/usage/demo.png)

![wip](data/usage/embeddings_annotated.png)

![wip](/data/usage/flow_topology.png)