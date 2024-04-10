import openai
from secret_key import openai_key
import json
import pandas as pd
openai.api_key = openai_key


def extract_financial_data(text):
    prompt = get_prompt_financial()+text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    content = response.choices[0]['message']['content']
    try:
        data = json.loads(content)
        return pd.DataFrame(data.items(), columns=["Measure", "Value"])
    except (json.JSONDecodeError, IndexError):
        pass

    return pd.DataFrame({
        "Measure": ["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"],
        "Value": ["", "", "", "", ""]
    })


def get_prompt_financial():
    return '''Please Retrieve company name,revenue,net income and earnings per share(a.k.a EPS) from the following article.
     If you can't find the information from this article then return "".
    Do not make things up.
    Then retrieve a stock sysmbol corresponding to that company.For this you can use
    your general knowledge(it doesn't have to be from this article).Always
    return your response as a valid JSON string.The format of the string should be this,
{
"Company Name": "Apple Inc",
"Stock Symbol":"AAPL"
"Revenue": $119.58 billion
"Net Income":  $100.913 billion
"EPS":"2.1 $"
}
News Article
=======================
'''

if __name__ == '__main__':
    text = '''Analysts project Dell's revenue to come in at $22.11 billion for the final quarter of fiscal 2024,
     a decline from the previous quarter and year-ago period amid a slump in the PC market, 
    according to estimates compiled by Visible Alpha.Net income is expected to be $1.26 billion, 
    down from $1.32 billion in the fiscal fourth quarter of 2023, while earnings per share (EPS) are projected at $1.72, 
    compared to $1.80 in the same period a year earlier.'''
    df = extract_financial_data(text)
    print(df.to_string())
