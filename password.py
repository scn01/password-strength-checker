import math   # Used for entropy calculation (log2)
import re     # Used for pattern detection (regex)

def calculate_entropy(password):

    # Dictionary holding all possible character sets
    charsets = {
        "lower": "abcdefghijklmnopqrstuvwxyz",
        "upper": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "digits": "0123456789",
        "symbols": "!@#$%^&*()-_=+[]{};:'\",.<>/?|`~"
    }

    R = 0  # Will store the character set size

    # Loops through each character set and checks if ANY character from the password appears in the charset
    for key, charset in charsets.items():
        if any(c in charset for c in password):
            R += len(charset)

    # If password is empty or something weird → avoid math error
    if R == 0:
        R = 1

    L = len(password)  # Length of password

    # Entropy formula using math.log2
    entropy = math.log2(R ** L)

    return round(entropy, 2)  # Round to 2 decimals for neat output

def check_repetition(password):

    # Regex: (.)\1{2,}
    # (.) captures any character
    # \1 means "the same character again"
    # \1{2,} means repeated at least 2 more times → total 3 in a row
    if re.search(r"(.)\1{2,}", password):
        return True

    # Check for repeated halves
    # Example: "abcabc" → first half "abc", second half "abc"
    half = len(password) // 2
    if password[:half] == password[half:]:
        return True

    return False

def strength_rating(entropy, has_repetition, length, variety_score):

    # If repeated patterns exist → automatic weak
    if has_repetition:
        return "Weak"

    # Strong password criteria
    if entropy > 60 and length > 12 and variety_score >= 3:
        return "Strong"

    # Medium criteria
    if entropy > 40 and length >= 8:
        return "Medium"

    # Anything else → weak
    return "Weak"

def password_strength(password):

    length = len(password)  # Length of the password

    variety_score = 0  # Max score = 4

    # Check lowercase letters
    if re.search(r"[a-z]", password):
        variety_score += 1

    # Check uppercase letters
    if re.search(r"[A-Z]", password):
        variety_score += 1

    # Check digits
    if re.search(r"[0-9]", password):
        variety_score += 1

    # Check symbols (anything NOT a letter or number)
    if re.search(r"[^A-Za-z0-9]", password):
        variety_score += 1

    # Call helper functions
    entropy = calculate_entropy(password)
    repeated = check_repetition(password)
    rating = strength_rating(entropy, repeated, length, variety_score)

    # Return a full report as a dictionary
    return {
        "Password": password,
        "Length": length,
        "Character Variety Score": f"{variety_score}/4",
        "Repeated Pattern Detected": repeated,
        "Entropy": entropy,
        "Strength Rating": rating
    }

password = input("Enter a password to evaluate: ")  # User enters password

# Analyze password
result = password_strength(password)

# Print report nicely
print("\n--- Password Strength Report ---")
for key, value in result.items():
    print(f"{key}: {value}")
