from src import generate_dataset, process_dataset

dataset = generate_dataset()
train_dataset,test_dataset = process_dataset(dataset=dataset)



