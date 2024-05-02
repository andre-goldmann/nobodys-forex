import logging
#import uvicorn
#from dotenv import load_dotenv
from fastapi import FastAPI, Request, status, Form
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
# Bellow the import create a job that will be executed on background
from fastapi.responses import JSONResponse
from transformers import AutoModelForCausalLM, AutoTokenizer
#import torch

#load_dotenv()
#app = FastAPI()

from transformers import T5ForConditionalGeneration, T5Tokenizer

def load_model():
    model = T5ForConditionalGeneration.from_pretrained('castorini/doc2query-t5-base-msmarco')
    tokenizer = T5Tokenizer.from_pretrained('castorini/doc2query-t5-base-msmarco')
    return model, tokenizer

def process_data(text, model, tokenizer):
    # Prepare the input text
    input_text = f"generate query: {text}"
    # Encode the input text
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    # Generate the output
    output = model.generate(input_ids, max_length=25, num_return_sequences=1)
    # Decode the output
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response



if __name__ == "__main__":

    # Load the model and tokenizer
    model, tokenizer = load_model()

    text = "how many people live in berlin"
    # Generate the output
    response = process_data(text, model, tokenizer)

    print("Response:")
    print(response)
    # Example: reuse your existing OpenAI setup






    #Base.metadata.create_all(engine)
    #port can only be 80 see tradingview
    #uvicorn.run(app, host="0.0.0.0", port=1280)