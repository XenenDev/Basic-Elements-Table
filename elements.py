import json

from openai import OpenAI
client = OpenAI(api_key="")


with open("/elements", 'r', encoding='utf-8') as f:
    elements = json.loads(f.read())["elements"]

new_elements = {}

cost = 0

for element in elements:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a providing hints to help a student deduct the element from its atomic symbol. Provide a short hint, like the use of that element. Just output the hint only."},
            {
                "role": "user",
                "content": element.get('name')
            }
        ]
    )
    hint = completion.choices[0].message.content
    cost += completion.usage.total_tokens
    print(cost, hint)
    new_elements[element.get('name')] = {'symbol': element.get('symbol'), 'number': element.get('number'), 'atomic_mass': element.get('atomic_mass'), 'hint': hint}

with open("/new_elements.json", 'w', encoding='utf-8') as f:
    f.write(json.dumps(new_elements))
