from google import genai
import pandas as pd


client = genai.Client(api_key="My API(can't show here)")


df = pd.read_csv("A_corporation_line_items_reclassified.csv")


summary = df.groupby('simplified_sector')['amount_crore'].sum().reset_index()
summary_string = summary.sort_values(by='amount_crore', ascending=False).to_string(index=False)


prompt = f"""
Act as an expert public finance analyst. I have reclassified the Chennai Corporation 
Budget so that ALL physical goods/assets are grouped under 'infrastructure', and services 
are kept in their original sectors.

Here is the new summary (in Crores):
{summary_string}

Please provide a 3-bullet-point summary of the city's spending priorities based on this new view.
"""


response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt
)

print("--- AI INSIGHTS ---")
print(response.text)
