import pickle

# Define a custom class for demonstration
class Table:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return f"Name: {self.name}, Value: {self.value}"

# Open the pickle file in read mode
with open('Table.pickle', 'rb') as file:
    # Load the pickled object
    data = pickle.load(file)
    
    # Check if the data is a list of custom objects
    if isinstance(data, list) and all(isinstance(item, Table) for item in data):
        # Iterate over the items in the list
        for index, obj in enumerate(data):
            # Print the object
            print(f"Index: {index}, Object: {obj}")
    else:
        print("The pickled object is not a list of MyObject instances.")


