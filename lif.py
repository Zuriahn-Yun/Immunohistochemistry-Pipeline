import os

"""
What could be useful
delete_lif


"""

def delete_lif(file_path):
    """ This will delete a lif file, they are typically very large and deleting them can save space to analyze another.

    Args:
        file_path (string): The local file path.
    """
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print("File at: " + str(file_path) + " removed successfully.")
        except Exception as e:
            print("Error " + str(e))
    else:
        print("File not found.")
            

