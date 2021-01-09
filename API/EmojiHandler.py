import re
from emot.emo_unicode import UNICODE_EMO, EMOTICONS

def convert_emojis(text):
    for emot in UNICODE_EMO:
        text = text.replace(emot, "_".join(UNICODE_EMO[emot].replace(",","").replace(":","").split()))
    return text

def convert_emoticons(text):
    for emot in EMOTICONS:
        text = re.sub(u'('+emot+')', "_".join(EMOTICONS[emot].replace(",","").split()), text)
    return text

text1 = "Hilarious 😂 :). The feeling of making a sale 😎, The feeling of actually fulfilling orders 😒"
text1 = convert_emojis(text1)
text1 = convert_emoticons(text1)
print(text1)