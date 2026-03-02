import pickle
from pprint import pprint

# Initialize an empty list to store the loaded objects
objects = []

# Open the pickle file in read-binary mode
with open('Table.pickle', 'rb') as file:
    while True:
        try:
            # Load the next object from the file
            objects.append(pickle.load(file))
        except EOFError:
            # Break the loop if the end of the file is reached
            break

# Pretty-print each object
for obj in objects:
    pprint(obj)

