import openai
import json

PROMPT = """
You will be given a list of tags used to describe a style of shirt. For example: Big Collar, Stripe Shirts, Green, etc...
Based on these tags, try to get an idea of what kind of style the shirt embodies.
Some of these tags will be too general to be usable, for example: Fashion Outfits, Top Outfits, Fashion Tips, etc...
Please do not take into account any tags which are too general and do not contain any information about the shirt that they describe.

Your response should contain 2 paragraphs. The first paragraph should be a short description of the style that the shirt embodies. The second parapgraph should be phrased as if you are instructing DALL-E to draw the shirt based on your description.

Here are the tags:
{tags}
"""

with open("./keys.json") as f:
    openai.api_key = json.load(f)["openai"]

def get_ai_stuff(tags):
    response = generate_response(tags).split("\n")
    image_urls = generate_image(response[2])
    return {"images": image_urls, "description": response[0]}

def generate_response(tags):
    return "Content"
    # generate response
    conversation = [
        {"role": "user", "content": PROMPT.format(tags = ",\n".join(tags))}
    ]
    print(PROMPT.format(tags = ",\n".join(tags)))
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
    )
    content = response['choices'][0]['message']['content']
    # return response
    return content

def generate_image(prompt):
    return "Link"
    response = openai.Image.create(
        prompt=prompt,
        n=2,
        size="512x512"
    )
    image_urls = []
    image_urls.append(response['data'][0]['url'])
    image_urls.append(response['data'][1]['url'])
    return image_urls