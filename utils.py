import json
from typing import List, Dict

class AnimeUtil:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save_animes(self, animes: List[Dict]):
        """Save the list of anime details to a JSON file."""
        try:
            with open(self.file_path, 'w') as file:
                json.dump(animes, file, indent=4)
            print("Animes have been saved successfully.")
        except IOError as e:
            print(f"An error occurred while saving the file: {e}")

    def load_animes(self) -> List[Dict]:
        """Load the list of anime details from a JSON file."""
        try:
            with open(self.file_path, 'r') as file:
                animes = json.load(file)
            print("Animes have been loaded successfully.")
            return animes
        except FileNotFoundError:
            print("No such file exists. Returning an empty list.")
            return []
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return []