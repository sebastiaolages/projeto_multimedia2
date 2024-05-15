import os
import time

def rle_encode(data):
    print("Iniciando a codificação RLE...")
    encoding = ''
    prev_char = ''
    count = 1

    if not data:
        return ''

    prev_char = data[0]
    for char in data[1:]:
        if char == prev_char:
            count += 1
        else:
            encoding += str(count) + prev_char
            count = 1
            prev_char = char

    encoding += str(count) + prev_char
    print("Codificação RLE completa.")
    return encoding

def rle_decode(data):
    print("Iniciando a decodificação RLE...")
    decode = ''
    count = ''
    for char in data:
        if char.isdigit():
            count += char
        else:
            if count:
                num_repeats = int(count)
                decode += char * num_repeats
                count = ''
            else:
                raise ValueError("Formato de dados de entrada inválido para RLE decode.")
    print("Decodificação RLE completa.")
    return decode

def read_file(file_path):
    print(f"Lendo o arquivo {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()
    except UnicodeDecodeError:
        with open(file_path, 'rb') as file:
            data = file.read().decode('utf-8', errors='ignore')
    print("Leitura de arquivo completa.")
    return data

def process_file(file_path):
    data = read_file(file_path)

    start_time = time.time()
    encoded_data = rle_encode(data)
    encode_time = time.time() - start_time
    print(f"Tempo de codificação: {encode_time} segundos.")

    start_time = time.time()
    decoded_data = rle_decode(encoded_data)
    decode_time = time.time() - start_time
    print(f"Tempo de decodificação: {decode_time} segundos.")

    original_size = len(data)
    compressed_size = len(encoded_data)
    compression_ratio = original_size / compressed_size if compressed_size else 0
    acl = (compressed_size * 8) / original_size

    return file_path, compression_ratio, acl, encode_time, decode_time

# Especificar o arquivo para processar
specific_file_path = r'C:\Users\sebas\PycharmProjects\project_multimedia2\CorpusSilesia\webster'
result = process_file(specific_file_path)
print(result)
