import random
import re
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import streamlit as st
import torch

model_name = "gpt2"  # You can also use "gpt2-medium" for a larger model
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

psychobabble = [
    [r'I need (.*)',
    ["Why do you need {0}?",
    "Would it really help you to get {0}?",
    "Are you sure you need {0}?"]],

    [r'Why don\'t you ([^\?]*)\??',
    ["Do you really think I don't {0}?",
    "Perhaps eventually I will {0}.",
    "Do you really want me to {0}?"]],

    [r'Why can\'t I ([^\?]*)\??',
    ["Do you think you should be able to {0}?",
    "If you could {0}, what would you do?",
    "I don't know -- why can't you {0}?",
    "Have you really tried?"]],

    [r'I can\'t (.*)',
    ["How do you know you can't {0}?",
    "Perhaps you could {0} if you tried.",
    "What would it take for you to {0}?"]],

    [r'I am (.*)',
    ["Did you come to me because you are {0}?",
    "How long have you been {0}?",
    "How do you feel about being {0}?"]],

    [r'I\'m (.*)',
    ["How does being {0} make you feel?",
    "Do you enjoy being {0}?",
    "Why do you tell me you're {0}?",
    "Why do you think you're {0}?"]],

    [r'Are you ([^\?]*)\??',
    ["Why does it matter whether I am {0}?",
    "Would you prefer it if I were not {0}?",
    "Perhaps you believe I am {0}.",
    "I may be {0} -- what do you think?"]],

    [r'What (.*)',
    ["Why do you ask?",
    "How would an answer to that help you?",
    "What do you think?"]],

    [r'How (.*)',
    ["How do you suppose?",
    "Perhaps you can answer your own question.",
    "What is it you're really asking?"]],

    [r'Because (.*)',
    ["Is that the real reason?",
    "What other reasons come to mind?",
    "Does that reason apply to anything else?",
    "If {0}, what else must be true?"]],

    [r'(.*) sorry (.*)',
    ["There are many times when no apology is needed.",
    "What feelings do you have when you apologize?"]],

    [r'Hello(.*)',
    ["Hello... I'm glad you could drop by today.",
    "Hi there... how are you today?",
    "Hello, how are you feeling today?"]],

    [r'I think (.*)',
    ["Do you doubt {0}?",
    "Do you really think so?",
    "But you're not sure {0}?"]],

    [r'(.*) friend (.*)',
    ["Tell me more about your friends.",
    "When you think of a friend, what comes to mind?",
    "Why don't you tell me about a childhood friend?"]],

    [r'Yes',
    ["You seem quite sure.",
    "OK, but can you elaborate a bit?"]],

    [r'(.*)\?',
    ["Why do you ask that?",
    "Please consider whether you can answer your own question.",
    "Perhaps the answer lies within yourself?",
    "Why don't you tell me?"]],

    [r'quit',
    ["Thank you for talking with me.",
    "Good-bye.",
    "Thank you, that will be $150. Have a good day!"]],

    [r'(.*)',
    ["Please tell me more.",
    "Let's change focus a bit... Tell me about your family.",
    "Can you elaborate on that?",
    "Why do you say that {0}?",
    "I see.",
    "Very interesting.",
    "{0}.",
    "I see.  And what does that tell you?",
    "How does that make you feel?",
    "How do you feel when you say that?"]]
]


def eliza_response(input_text):
    for pattern, responses in psychobabble:
        match = re.match(pattern, input_text.rstrip(".!"))
        if match:
            response = random.choice(responses)
            return response.format(*match.groups())
    return generate_response(input_text)

def generate_response(input_text):
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(input_ids, max_length=50, num_return_sequences=1)
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        return generated_text

def main():
    st.title("Evolved Eliza 1966 Chatbot with GPT-2")
    st.write("Hello, I'm the evolved Eliza 1966! How can I help you today?")

    user_input = st.text_input("You: ")
    if user_input:
        response = eliza_response(user_input)
        st.text("Evolved Eliza: " + response)
        
        

if __name__ == "__main__":
    main()
