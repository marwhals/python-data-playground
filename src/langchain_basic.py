import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from langchain_community.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch

# ✅ Tiny free model (text2text)
model_id = "google/flan-t5-small"

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
)

# Create pipeline (text2text generation)
generator = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=100,
    temperature=0.7,
    top_p=0.95,
)

# Wrap in LangChain
llm = HuggingFacePipeline(pipeline=generator)

# Prompt template (instruction-based)
prompt = PromptTemplate.from_template("Explain this like I'm five: {topic}")

# LangChain LLM chain
chain = LLMChain(llm=llm, prompt=prompt)

# Run it
response = chain.run("Biology")
print("GPU available:", torch.cuda.is_available())
print("Model device:", next(model.parameters()).device)

print(response)
