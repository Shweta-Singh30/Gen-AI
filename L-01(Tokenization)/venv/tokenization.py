import tiktoken

encoder=tiktoken.encoding_for_model('gpt-4o')


print("Vacab Size",encoder.n_vocab)
text="My name is Shweta"
tokens= encoder.encode(text)
print("Tokens", tokens)

my_tokens=[5444, 1308, 382, 1955, 138132]

decoded=encoder.decode([5444, 1308, 382, 1955, 138132])
print("Decoded",decoded)