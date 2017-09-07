text = "abc : [qwerty : 0x3354] poliuq [klmopn : 099]"
import re

# m = re.search(r"\[(\w+)\]", text)
# print m.group(1)
print text[text.rfind('[')+1:text.rfind(']')]