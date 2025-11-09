# Dictionary
import requests

def get_word_definition(word):
    """Looks up a word's definition from a dictionary website using an API."""
    # 1. Build the API URL for the word
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.strip().lower()}"

    print(f"\n--- Searching for the definition of: '{word}'...")

    try:
        # 2. Make the request to the website. We wait up to 10 seconds for a response.
        response = requests.get(url, timeout=10)

        # 3. Check if the request was successful (Status Code 200 means success)
        if response.status_code != 200:
            if response.status_code == 404:
                return f"Sorry! I couldn't find a definition for '{word}'. Try checking your spelling!"
            else:
                # For any other website error
                return f"Oops! There was a problem connecting (Code: {response.status_code})."

        # 4. If successful, convert the result from the website into Python data
        data = response.json()

        entry = data[0]

        # The data is organized: Meanings -> First Meaning -> Definitions -> First Definition
        try:
            # Get the actual word we found
            word_found = entry.get('word', 'Word Not Found')
            
            # Get the part of speech (like 'noun' or 'verb')
            part_of_speech = entry['meanings'][0]['partOfSpeech']
            
            # Get the actual definition text
            definition_text = entry['meanings'][0]['definitions'][0]['definition']
            
            # Put the final answer together
            output = f"\n*** {word_found.upper()} ***"
            output += f"\nPart of Speech: {part_of_speech}"
            output += f"\nDefinition: {definition_text}"
            return output

        except (IndexError, KeyError):
            # This catches errors if the definition is stored in a way we don't expect
            return f"I found the word '{word}', but couldn't read the definition clearly. Try another word."

    except requests.exceptions.RequestException:
        # This catches errors if there is no internet connection
        return "A network error occurred. Check your internet connection!"
    except Exception as e:
        # This catches any other unexpected error
        return f"An unexpected error occurred: {e}"

def main():
    print("---------------------------------------")
    print("      Simple Dictionary Finder!")
    print("---------------------------------------")
    print("Type a word to get its definition.")

    while True:
        # Get the word from the user
        user_input = input("\nEnter a word (or type 'q' to quit): ").strip()
        
        # Check if the user wants to quit
        if user_input.lower() in ['q', 'quit', 'exit']:
            print("\nThanks for using the dictionary! Happy learning.")
            break
        
        # Check if the user entered an empty line
        if not user_input:
            print("Please type a word before pressing Enter.")
            continue

        # Get and show the definition
        result = get_word_definition(user_input)
        print(result)

if __name__ == "__main__":
    main()