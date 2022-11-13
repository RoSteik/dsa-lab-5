import time

B = 13  # Константа в формулі хешування
Q = 256  # Кількість елементів в таблиці ICQ


def get_hash(pattern: str) -> int:
    global B, Q
    m = len(pattern)
    result = 0
    for i in range(m):
        result = (B * result + ord(pattern[i])) % Q  # схема Горнера + модульна арифметика

    return result


def search_patterns_in_text(text: str, patern: str) -> None:
    global B, Q
    pattern_len = len(patern)
    text_len = len(text)

    multiplier = 1
    for i in range(1, pattern_len):
        multiplier = (multiplier * B) % Q  # максильний степінь B - це потрібно для плаваючого хешу

    pattern_hash = get_hash(patern)
    text_hash = get_hash(text[:pattern_len])  # хеш першої підстроки, яка рівна довжині патерна в text

    count = 0  #  результат
    t0 = time.time()
    for index_symbol in range(text_len - pattern_len + 1):
        if pattern_hash == text_hash:
            if text[index_symbol: index_symbol + pattern_len] == patern:  # перевірка на колізію
                count += 1

        if index_symbol < text_len - pattern_len: # якщо true, ідемо далі - за плаваючим хешом
            text_hash = ((text_hash - ord(text[index_symbol]) * multiplier) * B
                         + ord(text[index_symbol + pattern_len])) % Q  # плаваючий хеш

            if text_hash < 0:
                text_hash += Q
    t1 = time.time()
    print(f"Result: {count}; The running time of the algorithm is equal to: {t1 - t0}")


pattern = "Voluptatem"
with open("text.txt", encoding="utf-8") as file_read:
    text = file_read.read()

search_patterns_in_text(text, pattern)
