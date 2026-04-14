import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import Dataset

# 1. Configuration
model_name = "microsoft/DialoGPT-small"
output_dir = "./custom_model"

# Detect Hardware
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

print(f"Loading custom model: {model_name}...")

# 2. Load Tokenizer and Base Model
tokenizer = AutoTokenizer.from_pretrained(model_name)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

# 3. Create a more "Advanced" Conversational Dataset
# We add eos_token after every turn so the model learns when to stop
eos = tokenizer.eos_token
data = {
    "text": [
        f"User: Hello{eos}Assistant: Hi! I am your advanced AI. How can I help?{eos}",
        f"User: What is your favorite color?{eos}Assistant: I like cyan, it feels very techy and modern!{eos}",
        f"User: Who created you?{eos}Assistant: I was fine-tuned by a powerful AI assistant!{eos}",
        f"User: Tell me a joke.{eos}Assistant: Why did the computer show up late to work? It had a hard drive!{eos}",
        f"User: kese ho{eos}Assistant: Main theek hoon, aapki madad ke liye taiyar!{eos}",
        f"User: what is FastAPI?{eos}Assistant: FastAPI is a modern, fast (high-performance) web framework for building APIs with Python.{eos}"
    ]
}

print("Preparing the dataset...")
dataset = Dataset.from_dict(data)

# 4. Tokenization Function
def tokenize_function(examples):
    inputs = tokenizer(examples["text"], padding="max_length", truncation=True, max_length=64)
    inputs["labels"] = inputs["input_ids"].copy()
    return inputs

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# 5. Training Arguments
# Increased complexity: added weight decay and better learning rate scheduler
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=2,           
    per_device_train_batch_size=3,
    save_steps=500,
    save_total_limit=1,
    logging_steps=1,
    learning_rate=3e-5,
    weight_decay=0.01,
    warmup_steps=1,
    fp16=False,                   # CPU doesn't support fp16 well
    remove_unused_columns=False,
    push_to_hub=False,
    report_to="none",
    dataloader_pin_memory=False   # Avoid the pin_memory warning on CPU
)

# 6. Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
)

# 7. Start Fine-tuning
print("Starting training (fine-tuning)...")
trainer.train()

# 8. Save the Customized Model and Tokenizer
print(f"Training complete. Saving custom model to {output_dir}")
os.makedirs(output_dir, exist_ok=True)
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)

print("Advanced model is now ready!")
