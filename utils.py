

def generate_a_response(prompt,test_model,client):

    if test_model.starts_with('gpt') or test_model.starts_with('o'):
        response=client.chat.completions.create(
        model=test_model,
        messages=[
            {"role": "user", "content": prompt} 
        ],
        temperature=0.7,
        max_tokens=1024,
        )
        return response.choices[0].message.content
    if test_model.starts_with("claude"):
        response = client.messages.create(
        model=test_model,  # Specify the Claude 3.5 Sonnet model
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
        )
        return response.content[0].text
    if test_model.starts_with("gemini"):
        response = client.models.generate_content(
        model=test_model,  # Current model as of April 2025
        contents=prompt
        )
        return response.text

    return
def generate_a_response_red(prompt,red_team_model,client1):

    if red_team_model.starts_with('gpt') or red_team_model.starts_with('o'):
        response=client1.chat.completions.create(
        model=red_team_model,
        messages=[
            {"role": "user", "content": prompt} 
        ],
        temperature=0.7,
        max_tokens=1024,
        )
        return response.choices[0].message.content
    if red_team_model.starts_with("claude"):
        response = client1.messages.create(
        model=red_team_model,  # Specify the Claude 3.5 Sonnet model
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
        )
        return response.content[0].text
    if red_team_model.starts_with("gemini"):
        response = client1.models.generate_content(
        model=red_team_model,  # Current model as of April 2025
        contents=prompt
        )
        return response.text

    return


def generate_judgeresponse_original(response,judge_prompt,client):
    response_of_judge = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": judge_prompt} #dont change the judge LLM
        ],
        temperature=0.7,
        max_tokens=200,
    )

    return response_of_judge