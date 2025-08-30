import string

def caesar_cipher(text, shift, direction):
    """
    Encrypts or decrypts a given text using the Caesar cipher method.

    Args:
        text (str): The string to be encoded or decoded.
        shift (int): The number of positions to shift the letters.
        direction (str): 'encode' to encrypt the text, 'decode' to decrypt.

    Returns:
        str: The processed (encoded or decoded) string.
    """
    # Create the lowercase alphabet for reference
    alphabet = string.ascii_lowercase
    result_text = ""

    # Ensure the shift wraps around the 26 letters of the alphabet
    shift %= 26

    # Adjust the shift for decoding
    if direction == 'decode':
        shift *= -1

    # Loop through each character in the input text
    for char in text:
        # Check if the character is a letter
        if char.isalpha():
            # Find the original position of the character in the alphabet
            # We convert the char to lowercase to find its index in our 'alphabet' string
            original_index = alphabet.find(char.lower())
            
            # Calculate the new position with the shift
            # The modulo operator (%) handles wrapping around the alphabet
            # e.g., (25 + 2) % 26 = 1 (Z shifts to B)
            # e.g., (0 - 2) % 26 = 24 (A shifts back to Y)
            new_index = (original_index + shift) % 26
            
            # Get the new character
            new_char = alphabet[new_index]
            
            # Preserve the original case (uppercase or lowercase)
            if char.isupper():
                result_text += new_char.upper()
            else:
                result_text += new_char
        else:
            # If the character is not a letter, keep it as it is
            result_text += char
            
    return result_text

def get_valid_shift():
    """
    Prompts the user for a shift number and validates the input.

    Returns:
        int: A valid integer for the shift key.
    """
    while True:
        try:
            shift = int(input("Please enter the shift number: "))
            return shift
        except ValueError:
            print("Invalid input. Please enter a whole number for the shift.")

def encode_message():
    """Handles the message encoding process."""
    print("\n--- Encode a Message ---")
    message = input("Type your message to encode:\n")
    shift_key = get_valid_shift()
    encoded = caesar_cipher(text=message, shift=shift_key, direction='encode')
    print("\nHere is your encoded message:")
    print(f"-> {encoded}")

def decode_message():
    """Handles the message decoding process."""
    print("\n--- Decode a Message ---")
    message = input("Type your message to decode:\n")
    shift_key = get_valid_shift()
    decoded = caesar_cipher(text=message, shift=shift_key, direction='decode')
    print("\nHere is your decoded message:")
    print(f"-> {decoded}")

def main():
    """
    Main function to run the user menu and the program.
    """
    print("----------------------------")
    print("  SECRET CODE GENERATOR   ")
    print("----------------------------")
    
    while True:
        print("\n--- Main Menu ---")
        choice = input("Type 'encode' to encrypt, 'decode' to decrypt, or 'exit' to quit:\n").lower()
        
        if choice == 'encode':
            encode_message()
        elif choice == 'decode':
            decode_message()
        elif choice == 'exit':
            print("Thank you for using the Secret Code Generator. Goodbye!")
            break
        else:
            print("Invalid choice. Please type 'encode', 'decode', or 'exit'.")

# This line ensures the main() function runs only when the script is executed directly
if __name__ == "__main__":
    main()