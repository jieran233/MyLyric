import mutagen  # Library for reading metadata from audio files
from Crypto.Cipher import AES  # Library for AES encryption/decryption
import base64  # Library for base64 encoding/decoding

music163_key_left = "163 key(Don't modify):"  # Prefix for the 163 key in metadata
secret_key = r"#14ljk_!\]&0U<'("  # Secret key used for AES decryption
decrypted_text_left = "music:"  # Prefix for the decrypted text

# Dictionary mapping file formats to the corresponding metadata key containing the 163 key
supported_formats_metadata = {
    'flac': 'description',  # Example: FLAC format uses 'description' tag
    'mp3': 'COMM::chs'  # Example: MP3 format uses 'COMM::chs' tag
}


def get_music163key(file: str):
    """
    Function to extract the 163 key from audio file metadata.

    Args:
        file (str): Path to the audio file.

    Returns:
        str: Extracted 163 key from the audio file metadata.

    Raises:
        Exception: If the audio file format is not supported.
    """
    file_extension = file.split('.')[-1].lower()  # Extract file extension
    if file_extension in supported_formats_metadata:
        format_key = supported_formats_metadata[file_extension]  # Get corresponding metadata key
        # Extract and clean the 163 key from the metadata
        return mutagen.File(file)[format_key][0].lstrip(music163_key_left)
    else:
        raise Exception('Unsupported audio file format')


def decrypt_aes(text, key):
    """
    Function to decrypt text using AES encryption.

    Args:
        text (str): Text to decrypt.
        key (str): Encryption key.

    Returns:
        str: Decrypted text.

    """
    key = key.encode('utf-8')  # Convert key to bytes
    cipher = AES.new(key, AES.MODE_ECB)  # Create AES cipher in ECB mode
    decrypted_text = cipher.decrypt(base64.b64decode(text))  # Decrypt text using base64 decoding
    # Remove special characters at the end (padding)
    decrypted_text = decrypted_text.rstrip(
        b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
        b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f')
    return decrypted_text.decode('utf-8')  # Convert decrypted bytes to string


def get_decrypted_music163key(file: str):
    """
    Function to extract and decrypt the 163 key from audio file metadata.

    Args:
        file (str): Path to the audio file.

    Returns:
        str: Decrypted 163 key.

    """
    music163_key = get_music163key(file)  # Extract 163 key from metadata
    decrypted_text = decrypt_aes(music163_key, secret_key)  # Decrypt the 163 key
    decrypted_text = decrypted_text.lstrip(decrypted_text_left)  # Remove prefix from decrypted text
    return decrypted_text  # Return decrypted 163 key
