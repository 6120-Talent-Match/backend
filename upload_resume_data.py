import pandas as pd
from datasets import Dataset, DatasetDict
from huggingface_hub import HfApi, login
from config import settings
from datasets import load_dataset

# Set your Hugging Face API token and repository name
HF_TOKEN = settings.HUGGING_FACE_API_KEY
REPO_ID = "C0ldSmi1e/resume-dataset"  # Replace with your username if needed


def main():
  # Step 1: Load the CSV file
  print("Loading CSV file...")
  df = pd.read_csv("./resume_data/train.csv")
  print(f"Loaded {len(df)} records from resume.csv")

  # Step 2: Convert to Hugging Face dataset
  print("Converting to Hugging Face dataset format...")
  # Create dataset with 'train' split
  train_dataset = Dataset.from_pandas(df)
  dataset_dict = DatasetDict({"train": train_dataset})

  # Step 3: Login to Hugging Face
  print("Logging in to Hugging Face...")
  login(token=HF_TOKEN)

  # Step 4: Push to Hugging Face Hub
  print(f"Uploading dataset to {REPO_ID}...")
  dataset_dict.push_to_hub(
      repo_id=REPO_ID,
      private=True
  )

  print(f"Dataset successfully uploaded to {REPO_ID}")
  print("You can now load it with:")
  print(f"""
from datasets import load_dataset

# Load the dataset
dataset = load_dataset("{REPO_ID}", split="train")

# Check the first few rows
print(dataset.column_names)
print(dataset[0])
""")

  # Confirm the data is actually there
  dataset = load_dataset("C0ldSmi1e/resume-dataset", split="train")
  print(len(dataset))
  print(dataset.column_names)


if __name__ == "__main__":
  main()
