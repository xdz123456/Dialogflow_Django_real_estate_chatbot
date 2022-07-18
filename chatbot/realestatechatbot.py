from google.cloud.dialogflowcx_v3.types.agent import Agent
from google.cloud import dialogflowcx_v3
from google.protobuf.json_format import MessageToDict
import time


# Set the api key
# import os
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'google_cloud.json'


# Set global value
LOCATION = "global"
PROJECT_ID = "realestatechatbot-353821"


# For reuse the client
agent_client = dialogflowcx_v3.AgentsClient()
session_client = dialogflowcx_v3.SessionsClient()


# Create agent
def create_agent(display_name):
    parent = "projects/" + PROJECT_ID + "/locations/global"

    agent = Agent(
        display_name=display_name,
        default_language_code="en",
        time_zone="Europe/London",
    )

    response = agent_client.create_agent(request={"agent": agent, "parent": parent})

    return response


# For dialogflow cx, we can not get the agent directly
# I create a function to obtain the agent name
def get_agent_name(index_of_agent):
    # Initialize request argument(s)
    request = dialogflowcx_v3.ListAgentsRequest(
        parent="projects/" + PROJECT_ID + "/locations/global",
    )

    # Make the request
    agent_list = agent_client.list_agents(request=request)

    agent_str_list = []
    for res in agent_list:
        agent_str_list += [res.name]

    # Deal with the string
    for n in range(0, len(agent_str_list)):
        count = -1
        name = agent_str_list[n]
        for i in range(0, len(name)):
            if name[i] == '/':
                count = i
        if count == -1:
            agent_str_list[n] = name
        else:
            agent_str_list[n] = name[count + 1:]

    return agent_str_list[index_of_agent]


# Set up the agent name and session name
# Use current time as the session name
agent_name = get_agent_name(0)
SESSION_NAME = str(time.time())
session = session_client.session_path(PROJECT_ID, LOCATION, agent_name, SESSION_NAME)


# input is the input text from the web page
# Use the dialogflow cx to get the intent name detected, parameters and response text
def chat_with_me(input_text):

    # Call dialogflow's query input
    query_input = dialogflowcx_v3.QueryInput()
    query_input.text.text = input_text
    query_input.language_code = "en"

    request_detect = dialogflowcx_v3.DetectIntentRequest(
        session=session,
        query_input=query_input,
    )

    response_detect = session_client.detect_intent(request=request_detect)
    # Transform the response from DetectIntentResponse to json
    response_json = MessageToDict(response_detect._pb)

    # If have expected intend, Return the Parameter
    my_parameter = None
    intent_name = None
    output_text = " "

    # Obtain the parameter from the input text
    try:
        intent_name = response_json["queryResult"]["intent"]["displayName"]
        if intent_name == "Sell_City" or intent_name == "Buy_City":
            my_parameter = response_json["queryResult"]["parameters"]["my_city"]
        if intent_name == "Sell_Address":
            my_parameter = response_json["queryResult"]["parameters"]["my_address"]
        if intent_name == "Sell_Postcode" or intent_name == "Buy_Postcode":
            my_parameter = response_json["queryResult"]["parameters"]["my_postcode"]
        if intent_name == "Sell_Type" or intent_name == "Buy_Type":
            my_parameter = response_json["queryResult"]["parameters"]["my_type"]
        if intent_name == "Sell_BedroomNum" or intent_name == "Buy_BedroomNum":
            my_parameter = response_json["queryResult"]["parameters"]["my_bedroom_num"]
        if intent_name == "Sell_Price" or intent_name == "Buy_Min_Price" or intent_name == "Buy_Max_Price":
            my_parameter = response_json["queryResult"]["parameters"]["my_price"]
    except KeyError:
        print("No Detect intent")

    # Show the intent name and parameter on terminal
    print(intent_name)
    print("Parameter", my_parameter)

    # Deal with No Response Error
    length_of_response = len(response_detect.query_result.response_messages[0].text.text)
    if length_of_response > 0:
        output_text = response_detect.query_result.response_messages[0].text.text[0]

    return intent_name, my_parameter, output_text
