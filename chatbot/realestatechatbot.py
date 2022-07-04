from google.cloud.dialogflowcx_v3.types.agent import Agent
from google.cloud import dialogflowcx_v3
import os

# Set global value
LOCATION = "global"
SESSION_NAME = "me"
PROJECT_ID = "realestatechatbot-353821"
# Set the api key
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'google_cloud.json'

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


agent_name = get_agent_name(0)


def chat_with_me(input_text):
    session = session_client.session_path(PROJECT_ID, LOCATION, agent_name, SESSION_NAME)

    query_input = dialogflowcx_v3.QueryInput()
    query_input.text.text = input_text
    query_input.language_code = "en"

    request_detect = dialogflowcx_v3.DetectIntentRequest(
        session=session,
        query_input=query_input,
    )

    response_detect = session_client.detect_intent(request=request_detect)
    output_text = response_detect.query_result.response_messages[0].text.text[0]

    # print("Response fulfill text:", response_detect.query_result.response_messages[0].text.text[0])
    # print("Init query:", response_detect.query_result.text)
    # print("Detected intent:", response_detect.query_result.intent.display_name)
    # print("Detected intent confidence:", response_detect.query_result.intent_detection_confidence)
    return output_text

