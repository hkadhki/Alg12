import struct
from collections import Counter, defaultdict
import heapq
from PIL import Image

class Node:
    def __init__(self, value=None, freq=0, left=None, right=None):
        self.value = value
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_tree(frequency):
    heap = [Node(value=value, freq=freq) for value, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)

    return heap[0]

def generate_codes(tree, prefix="", code_map=None):
    if code_map is None:
        code_map = {}

    if tree.value is not None:
        code_map[tree.value] = prefix
    else:
        generate_codes(tree.left, prefix + "0", code_map)
        generate_codes(tree.right, prefix + "1", code_map)

    return code_map

def load(file_path):
    with Image.open(file_path) as img:
        img = img.convert("L")
        pixels = list(img.getdata())
        width, height = img.size
        return pixels, width, height


bmp_file = "A.bmp"

pixels, width, height = load(bmp_file)
frequency = Counter(pixels)
huffman_tree = build_tree(frequency)
huffman_codes = generate_codes(huffman_tree)

print(huffman_codes)