import os
import pandas as pd
import PIL.Image
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
load_dotenv()

genai.configure(api_key=os.getenv("AIzaSyCDJ_7QhyEHjf2epjq_qyVbF3nQmzPt4R8"))
img = PIL.Image.open("E:\\ieee\\vqa\\report_generation\\crack.jpeg")

# Data from the depth model
depth = "0.9 inch"

# Getting more information about the crack using VQA model:
model = genai.GenerativeModel('gemini-pro-vision')

question = "What is the material of this structure?"
response = model.generate_content([question, img], stream=True)
response.resolve()
material = response.text
print("Material: ", material)

question = "What is the length of this crack?"
response = model.generate_content([question, img], stream=True)
response.resolve()
length = response.text
print("Length: ", length)

question = "What is the width of this crack?"
response = model.generate_content([question, img], stream=True)
response.resolve()
width = response.text
print("Width: ", width)

question = f"""We know that the length of this crack is {length}, 
width of the crack is {width}, and the depth of the crack is {depth}. 
What is the serverity of this crack? Answer with Low, Medium, High or Critical."""
response = model.generate_content([question, img], stream=True)
response.resolve()
severity = response.text
print("Severity: ", severity)

question = f"""We know that the length of this crack is {length},
width of the crack is {width}, the depth of the crack is {depth} 
and the serverity of the crack is {severity}. What is the urgency of repair? 
Answer with Immediate, Urgent, Non-Critical, Critical, or Monitor."""
response = model.generate_content([question, img], stream=True)
response.resolve()
urgency = response.text
print("Urgency of repair: ", urgency)

question = f"""We know that the length of this crack is {length}, 
width of the crack is {width}, the depth of the crack is {depth}, the serverity of the crack is {severity} 
and urgency of repair is {urgency}. Taking these factors into consideration, What is the predicted future pattern of the crack?"""
response = model.generate_content([question, img], stream=True)
response.resolve()
pred_pattern = response.text
print("Future Predicted Pattern: ", pred_pattern)

question = f"""The length of the given crack is {length}, width of the crack is {width}, the depth of the crack is {depth}, the severity is {severity} and urgency of repair is {urgency}.
The following is also known about the crack's predicted pattern in the future: {pred_pattern}. Suggest a type of repair for this crack."""
response = model.generate_content([question, img], stream=True)
response.resolve()
cost = response.text
print("Repair Type: ", cost)


# Report Generation:
from datetime import datetime
now = datetime.now()
date = now.strftime("%d/%m/%Y %H:%M:%S")
weather = "Sunny"
location = "Coimbatore, India"

genai.configure(api_key=os.getenv("AIzaSyB8J912JdjSOFTZKC9md7TXvUcpc3z74CU"))
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["prompt2 = '''You will be provided with specific details about a crack, including its length, width, depth, material, severity, urgency of repair, predicted pattern of the crack in the future and type of repair. Additionally, you will receive general inspection details such as the date of inspection and weather conditions. Your task is to use this information to generate a markdown report. The report should consist of two main sections: \"Crack Details\" and \"Crack Description\".In the \"Crack Details\" section, create a markdown table that includes the following columns: Material of the Structure, Length, Width, Depth, Severity, Urgency of Repair, Predicted Pattern in the Future and Type of Repair. ```### Crack Details| Material of the Structure | Length | Width | Depth | Severity | Urgency of Repair | Predicted Future Pattern | Type of Repair | ------------------------- | ------ |------ | ----- | -------- | ----------------- |----------------- | ----------------- | [Material]                | [Length] | [Width] | [Depth] | [Severity] | [Urgency] | [Predicted Future pattern] | [Type of Repair] |```Under the \"Crack Description\" section, generate a paragraph description with a minimum of 200 words that includes the date of inspection, weather conditions, and the specific crack details provided.\n\nGenerated Markdown Output:```### Crack Details| Material of the Structure | Length | Width | Depth | Severity | Urgency of Repair | Predicted Future pattern | Type of Repair | ------------------------- | ------ | ------ | ----- | -------- | ----------------- | ----------------- |----------------- |----------------- | [Material]                | [Length] | [Width] | [Depth] | [Severity] | [Urgency] | [Predicted Future Pattern]  [Type of Repair] |### Crack Description [Generated 200 word paragraph description using the provided details.]``` \nDont include ``` and \\n in the output'''"]
  },
  {
    "role": "model",
    "parts": ["### Crack Details\n| Material of the Structure | Length | Width | Depth | Severity | Urgency of Repair |  Predicted Future Pattern | Type of Repair |\n| ------------------------- | ------ | ------ | ----- | -------- | ----------------- | ----------------- | ----------------- |\n| [Material]                 | [Length] | [Width] | [Depth] | [Severity] | [Urgency] | [Predicted Future Pattern] | [Type of Repair] |\n\n### Crack Description\n[Generated 200 word paragraph description using date, location and crack details.]"]
  },
])

convo.send_message(f"""Date is {date}, weather conditions are {weather}, and the location is {location}.
Material composition of the crack is {material}, length of the crack is {length}, width of the crack is {width},
depth of the crack is {depth}, severity of the crack is {severity}, urgency of repair is {urgency}, the predicted
future pattern of the crack is {pred_pattern} and the type of repair suggested is {cost}.""")
mark = convo.last.text

# Streamlit
st.markdown("## **Crack Report**")
col1, col2, col3 = st.columns([0.2, 5, 0.2])
col2.image(img ,width=500 , use_column_width=True)
df = pd.DataFrame({"Length":[59],"Width": [0.25], "Depth": [0.9]})
st.bar_chart(df)
st.markdown(mark)