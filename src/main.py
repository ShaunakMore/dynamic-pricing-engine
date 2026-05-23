from src.data_pipeline.generate_dataset import generate_dataset
from src.data_pipeline.process_dataset import process_dataset
from src.training.train import train_model
from src.training.evaluate import evaluate_model


dataset = generate_dataset()
print(f"Dataset of size: {len(dataset)} generated successfully.")

train_dataset,test_dataset = process_dataset(dataset=dataset)
print(f"Train and Test datasets of size: {len(train_dataset)}, {len(test_dataset)} generated successfully.")

train_model(train_dataset=train_dataset,test_dataset=test_dataset,model_save_path="./models/lightgbm_dynamic_pricing.pkl")

evaluate_model(test_dataset=test_dataset,model_save_path="./models/lightgbm_dynamic_pricing.pkl")
