#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os, getpass
import pprint
os.environ['OPENAI_API_KEY'] = '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'
os.environ['LANGCHAIN_API_KEY'] = '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'
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['TAVILY_API_KEY'] = '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'

# def _set_env(var: str):  # This is to check if you have set the required environment variables
#     if not os.environ.get(var):
#         os.environ[var] = getpass.getpass(f"{var}: ")
#
# _set_env("OPENAI_API_KEY")


from langchain_openai import ChatOpenAI
from IPython.display import Image, display
from typing import Any
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


# gpt4o_chat = ChatOpenAI(model="gpt-4o", temperature=0)
# gpt35_chat = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)


# In[119]:


class State(TypedDict):
    state: str
    notes: str
    question: str
    query: str
    response: str


class SummarizeInput:
    def __init__(self, state):
        # Initialize with state
        self.context = None
        self.summary = None

    def __call__(self, state):  # Accept state as an argument
        self.context = "Make a meeting minutes email with a summary a section and a next steps section from the following notes: " + state['state'][0]

        # Debugging: print the context before invoking the model
        print("Context being passed to the model:", self.context)

        # Invoke the model
        try:
            self.summary = gpt4o_chat.invoke(self.context)
        except Exception as e:
            print(f"Error invoking the model: {e}")
            self.summary = None

        # Debugging: check if summary is None or not
        if self.summary is not None:
            print("Summary:", self.summary)
        else:
            print("Summary is None, there was an error processing.")

        return {"state": [self.summary] if self.summary else ["No valid summary"]}



# In[ ]:


import requests
from bs4 import BeautifulSoup
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import initialize_agent, AgentType
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate


# In[ ]:


import requests
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate


# In[ ]:


# Set up the OpenAI LLM model (ensure you have the OpenAI API key set)
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Define a prompt template for the agent
prompt_template = """
You are a expert researcher tasked with gathering information for a client.
Your current objective is to gather documents about a product that the client wants to implement.
Here is the context you need to use to answer the query:

Context:
{context}

Question:
{question}

The answer should be in an email format that has a summary section that summarizes the current state first and a next steps section with action items.

Use bullet points. Use the following as an example:
Summary of current state
-topic 1
    -current state of this topic
-topic 2
    -current state of this topic

Next steps
    -action item for each topic. Include who is responsible for completing the action item

Answer:
"""

prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)
# llm_chain = LLMChain(prompt=prompt, llm=llm) # Deprecated method
# Use the new RunnableSequence to chain the prompt and the LLM together
runnable_sequence = prompt | llm


# In[ ]:


def fetch_web_content_with_tavily(query: str, num_results: int = 10):
    # Initialize TavilySearchResults (with your Tavily API key)
    tavily_search = TavilySearchResults(api_key="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", max_results=num_results)
    
    # Provide the tool input as a dictionary with 'query' and 'num_results'
    tool_input = {
        "query": query,
        "max_results": num_results,
        #"search_depth": "advanced",
    }
    
    # Perform the search query (use run method with tool_input)
    search_results = tavily_search.run(tool_input)
    print("len of search: ", len(search_results))

    all_content = []
    
    # Extract the content from the results
    for result in search_results:
        url = result["url"]
        print(url)
        response = requests.get(url)
        
        if response.status_code == 200:
            # Parse the page content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            page_content = " ".join([para.get_text() for para in paragraphs])
            all_content.append(page_content)

    return "\n\n".join(all_content)


# In[120]:


def query_with_web_context(state_dict):
    query = state_dict['query']
    question = state_dict['question']
    # Fetch content from the web using Tavily search
    web_content = fetch_web_content_with_tavily(query)
    
    if web_content:
        # Generate an answer using the new RunnableSequence (prompt | llm), passing the web content as context
        response = runnable_sequence.invoke({"context": web_content, "question": question})
        # return response
        return {'response': response}
    else:
        return "Could not retrieve content from the search results."


# In[115]:


# def generate_question(notes, question):
def generate_question(state: State):
    #question format: How to set up <what needs to be done> in <PaaS/IaaS service name>
    # * May have to format notes to be a single paragrapgh, with continuous sentences. 
    tavily_query = "How do you set up " + state['question'] + ", using only documents from docs.oracle.com"
    q = state['notes'] + ". Analyze the previous context and generate a plan to set up " + state['question']
    result = {'query': tavily_query,
            'question': q
           }
    return result


# In[116]:


def find_help(gen_question_dict):
    # function would need to hook up to Oracle's aria or some sort of directory. This is to find experts specializing in your question. 
    print('in find help')
    # return null


def format_response(query_with_web_context_response):
    # take response from find_help and query_with_web_context and summarize it to give the user succinct next steps
    print('in format response')
    return query_with_web_context_response


# In[121]:


# Building the graph
builder = StateGraph(State)
builder.add_node("Generate Question", generate_question)
builder.add_node("Query with Web Context", query_with_web_context)
builder.add_node("Find Help", find_help) # function would need to hook up to Oracle's aria or some sort of directory. This is to find experts specializing in your question. 
builder.add_node("Format Final Response", format_response)

# Building the flow
builder.add_edge(START, "Generate Question")
builder.add_edge("Generate Question", "Query with Web Context")
builder.add_edge("Generate Question", "Find Help")
builder.add_edge("Query with Web Context", "Format Final Response")
builder.add_edge("Find Help", "Format Final Response")
builder.add_edge("Format Final Response", END)
graph = builder.compile()


# In[110]:


display(Image(graph.get_graph().draw_mermaid_png()))


# In[127]:


# a = graph.invoke({
#     "notes": "The customer has an OAC instance provisioned",
#     "question": "access security for catalog items and dashboards in oracle analytics cloud."
#     })

a = graph.invoke({
    "notes": "vcn and subnets are provisioned",
    "question": "fastconnect."
    })

pprint.pprint(a)

