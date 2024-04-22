import json
import heapq
from collections import defaultdict
from datetime import datetime
import os
import math

class HuffmanCoding:
    def __init__(self):
        self.huffman_code = None

    def generate_huffman_code(self, text):
        frequency = defaultdict(int) #словарь типа defaultdict

        #проход по славорю с увеличением узлов
        for char in text: 
            frequency[char] += 1
        
        #создания heap некого списка списков
        heap = [[weight, [symbol, ""]] for symbol, weight in frequency.items()]
        #необхадимая строка для создания min-heap
        heapq.heapify(heap)

        while len(heap) > 1:
            lo = heapq.heappop(heap) #извлечение с минимальными частотами(узлами)
            hi = heapq.heappop(heap)
            for pair in lo[1:]: #левый узел дерева
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:#правый узел
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:]) #конечный узел со всей суммой

        self.huffman_code = sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))#сортированный по длине и самому коду

    def save_huffman_code_to_json(self):
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        folder_name = f"{timestamp}"
        os.makedirs(folder_name, exist_ok=True)

        code_file_path = os.path.join(folder_name, "code.json")

        with open(code_file_path, "w") as code_file:
            json.dump(dict(self.huffman_code), code_file, ensure_ascii=False, indent=4)

        print(f"Код Хаффмана сохранен в: {code_file_path}")

    def decode_huffman(self, encoded_text):
        reversed_huffman_code = {code: char for char, code in dict(self.huffman_code).items()}
        decoded_text = ""
        current_code = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in reversed_huffman_code:
                #если текущий код есть в обратном отображении, соответствующий ему символ добавляется к раскодированному тексту
                decoded_text += reversed_huffman_code[current_code]
                current_code = ""

        return decoded_text

def calculate_entropy(file_path):
    with open(file_path, 'rb') as file:
        byte_freq = {}
        total_bytes = 0
        byte = file.read(1)
        while byte:
            total_bytes += 1
            byte_freq[byte] = byte_freq.get(byte, 0) + 1
            byte = file.read(1)

        entropy = 0
        for freq in byte_freq.values():
            probability = freq / total_bytes
            entropy -= probability * math.log2(probability)

        return entropy

def calculate_file_size(file_path):
    return os.path.getsize(file_path)

def calculate_compression_ratio(original_size, compressed_size):
    return original_size / compressed_size
