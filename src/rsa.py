import random


def is_prime(n: int) -> bool:
    """
    Check if a number is prime.

    :param n: The number to check.
    :type n: int

    :return: True if the number is prime, False otherwise.
    :rtype: bool
    """
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def generate_n_digit_prime(n_digits: int = 2) -> int:
    """
    Generate a random n-digit prime number.

    :param n_digits: The number of digits the prime number should have. Must be positive.
    :type n_digits: int

    :return: A random double-digit prime number.
    :rtype: int

    :raises AssertionError: If n_digits is not positive.
    """
    assert n_digits > 0, f'{n_digits} is not positive.'

    n_digit_number = lambda n: random.randint(10 ** (n - 1), 10 ** n - 1)
    prime = n_digit_number(n_digits)
    while not is_prime(prime):
        prime = n_digit_number(n_digits)
    return prime


def gcd(a: int, b: int) -> int:
    """
    Calculate the greatest common divisor of two numbers.

    :param a: The first number. Must be positive.
    :type a: int
    :param b: The second number. Must be positive.
    :type b: int

    :return: The greatest common divisor of a and b.
    :rtype: int

    :raises AssertionError: If a or b is not positive.
    """
    assert a > 0, f'{a} is not positive.'
    assert b > 0, f'{b} is not positive.'

    while b != 0:
        a, b = b, a % b
    return a


def mod_inverse(a: int, m: int) -> int:
    """
    Calculate the modular inverse of a modulo m.

    :param a: The number to calculate the modular inverse of. Must be positive.
    :type a: int
    :param m: The modulo. Must be positive.
    :type m: int

    :return: The modular inverse of a modulo m.
    :rtype: int

    :raises AssertionError: If a or m is not positive, or if a and m are not relatively prime.
    """
    assert a > 0, f'{a} is not positive.'
    assert m > 0, f'{m} is not positive.'
    assert gcd(a, m) == 1, f'{a} and {m} are not relatively prime.'

    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1


def generate_keypair(d: int = 2) -> ((int, int), (int, int)):
    """
    Generate public and private keys.

    :param d: The number of digits the prime numbers should have. Must be positive. Optional, defaults to 2.
    :type d: int

    :return: A tuple containing the public and private keys in the form (n, e) and (n, d) respectively.
    :rtype: tuple[tuple[int, int], tuple[int, int]]
    """
    p = generate_n_digit_prime(d)
    q = generate_n_digit_prime(d)

    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose e such that 1 < e < phi and gcd(e, phi) = 1
    e = random.randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    # Calculate d, the modular inverse of e modulo phi
    d = mod_inverse(e, phi)

    public_key = (n, e)
    private_key = (n, d)

    return public_key, private_key


def encrypt(message: str, public_key: (int, int)) -> str:
    """
    Encrypt a message using RSA.

    :param message: The message to encrypt.
    :type message: str
    :param public_key: The public key to encrypt the message with.
    :type public_key: tuple[int, int]

    :return: The encrypted message.
    :rtype: str
    """
    n, e = public_key
    cipher_text = ','.join([str((ord(char) ** e) % n) for char in message])
    return cipher_text


def decrypt(cipher_text: str, private_key: (int, int)) -> str:
    """
    Decrypt a message using RSA.

    :param cipher_text: The message to decrypt.
    :type cipher_text: str
    :param private_key: The private key to decrypt the message with.
    :type private_key: tuple[int, int]

    :return: The decrypted message.
    :rtype: str
    """
    n, d = private_key
    cipher_text = [int(char) for char in cipher_text.split(',')]
    decrypted_message = ''.join([chr((char ** d) % n) for char in cipher_text])
    return decrypted_message
