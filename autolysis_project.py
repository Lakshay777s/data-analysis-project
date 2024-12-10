# -*- coding: utf-8 -*-
"""autolysis_project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gF_hnn7kqoqMNOg5H8OGPf2IdOEi2wqW
"""

!pip install pandas seaborn matplotlib openai

!pip install openai==0.27.8

import pandas as pd
import os
import openai
import seaborn as sns
import matplotlib.pyplot as plt
from google.colab import files


uploaded = files.upload()

filename = list(uploaded.keys())[0]
data = pd.read_csv(filename)

print("Dataset Summary:")
print(data.info())
print("\nBasic Statistics:")
print(data.describe())

missing_values = data.isnull().sum()
print("\nMissing Values:")
print(missing_values)

os.environ["AIPROXY_TOKEN"] = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIyZjEwMDA2MTlAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.vJ1FSaBopE8Cf4vKslSBxfXe1ZlfwBCPCQzmg8o6aTc"

openai.api_base = "https://aiproxy.sanand.workers.dev/openai/v1"

def query_llm(prompt):
    openai.api_key = os.getenv("AIPROXY_TOKEN")
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

columns = data.columns.tolist()
sample_data = data.sample(5).to_dict()
prompt = f"""
I have a dataset with the following columns: {columns}.
Here is a sample of the data: {sample_data}.
What are some analyses I can perform on this dataset? Provide Python code examples.
"""
llm_response = query_llm(prompt)
print("LLM Suggestions:")
print(llm_response)

numeric_data = data.select_dtypes(include=["number"])
correlation_matrix = numeric_data.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.savefig("correlation_heatmap.png")
plt.show()

analysis_results = {
    "summary": data.describe().to_dict(),
    "missing_values": missing_values.to_dict()
}
prompt_story = f"""
Here's my dataset analysis: {analysis_results}.
Please narrate a story explaining the data, the analysis, and key findings.
Include suggestions for potential use cases or next steps.
"""
story = query_llm(prompt_story)

with open("README.md", "w") as f:
    f.write("# Dataset Analysis Report\n\n")
    f.write(story)
    f.write("\n\n![Correlation Heatmap](correlation_heatmap.png)\n")

files.download("README.md")
files.download("correlation_heatmap.png")