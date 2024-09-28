from openai import OpenAI

def generate_image_from_text(client, prompt, size="1024x1024"):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

def generate_text_from_prompt(client, prompt, model="gpt-4o", max_tokens=256):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt + "(請用正體中文(zh_TW)回答)"
                }
            ],
            temperature=1,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        message_content = response.choices[0].message.content
        return message_content
    except Exception as e:
        print(f"Error generating text: {e}")
        return None

def create_openai_client():
    return OpenAI()