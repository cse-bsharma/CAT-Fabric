# Open the file for reading
with open("query_tpcds.txt", "r") as file:
    # Read the entire contents of the file into a variable
    file_contents = file.read()

# Now, the variable 'file_contents' holds the content of the file
print(file_contents)
