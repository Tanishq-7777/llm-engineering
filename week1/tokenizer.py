import tiktoken

encoding = tiktoken.encoding_for_model("gpt-4.1")

tokens = encoding.encode("hey there was a missunderstanding")
print(tokens)