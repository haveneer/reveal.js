from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from openai import OpenAI
from translate_one_section import translate_one_section
import hashlib
import time

max_conversion = 200
interval = 1  # seconds between 2 queries


# see also (about custom functions): https://gokhang1327.medium.com/getting-started-with-the-openai-api-chatgpt-in-python-d689eecbbd37

def remove_whitespace(input_string):
    return "".join(input_string.split())


if __name__ == '__main__':
    load_dotenv()
    client = OpenAI()
    client.api_key = os.getenv("OPENAI_API_KEY")

    # pricing: https://openai.com/api/pricing/
    model = "gpt-4"
    # model = "gpt-3.5-turbo"
    assert model in [model.id for model in client.models.list()]
    # for m in client.models.list():
    #     print(m)

    with open("/Users/pascal/haveneer/reveal.js/slides/SoftwareEngineering/index_translated.html") as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    sections = soup.find_all("section")
    count = 0

    for section in sections:
        if section.section is not None:
            continue
        if section.h2 is not None and "class" in section.h2.attrs and "title" in section.h2.attrs["class"]:
            if "class" in section.attrs and "translated" in section.attrs["class"]:
                continue
            if "class" in section.attrs and "skip-translate" in section.attrs["class"]:
                continue
            if "class" in section.attrs and "hidden" in section.attrs["class"]:
                continue
            if count >= max_conversion:
                break

            print(len(str(section)), str(section).replace("\n", " ")[0:80])
            # for x in section.children:
            #     print("*: ",str(x).replace("\n", " ")[0:50])

            replacement = translate_one_section(client, model, str(section))
            checksum = hashlib.md5(remove_whitespace(str(section)).encode('utf-8')).hexdigest()
            replacement = BeautifulSoup(replacement, 'html.parser').section
            if "class" in replacement.attrs:
                replacement.attrs["class"].append("translated")
            else:
                replacement.attrs["class"] = ["translated"]
            replacement.attrs["translation-hash"] = checksum
            section.replace_with(replacement)
            # section.extract() # remove section
            count += 1

            with open("/Users/pascal/haveneer/reveal.js/slides/SoftwareEngineering/index_translated.html",
                      mode="w",
                      encoding='utf-8') as fp:
                fp.write(str(soup.prettify()))
            time.sleep(interval)

    print(f"count = {count}")
    # with open("/Users/pascal/haveneer/reveal.js/slides/SoftwareEngineering/index_translated.html", "w",
    #           encoding='utf-8') as fp:
    #     fp.write(str(soup.prettify()))
