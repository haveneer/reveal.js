dry_run = False


def translate_one_section(client, model, section) -> str:
    pre_prompt = ("You are a helpful assistant designed to translate technical HTML slides from English to French.\n"
                  "Do not translate HTML tags or their attributes, HTML comments, links, URLs, or pieces of code.\n"
                  "English technical words that are commonly used also in French can remain as they are in English "
                  "using quotes around them.")

    if dry_run:
        return '<section><h1 class="em boldest">Translation placeholder</b></section>'
    else:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": pre_prompt},
                {"role": "user", "content": section}
            ],
            temperature=0.1,
            max_tokens=4096,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return completion.choices[0].message.content
