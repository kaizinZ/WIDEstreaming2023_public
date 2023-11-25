import random
import string

from tqdm import tqdm


def create_dummy_file(filepath, max_file_size, block_size=1024 * 1024):
    file_size = max(random.randint(10240, max_file_size), 10240)  # 10KB以上のランダムなサイズ

    with open(filepath, "w") as f:
        remaining_size = file_size
        while remaining_size > 0:
            chunk_size = min(block_size, remaining_size)
            line = ''.join(random.choices(string.ascii_letters + string.digits, k=chunk_size))
            f.write(line)
            remaining_size -= chunk_size

def main():
    for i in tqdm(range(30)):
        dummy_file_path = f'./dummies/dummy_{i}.txt'
        create_dummy_file(dummy_file_path, 250 * (1024 ** 2))

if __name__ == '__main__':
    main()