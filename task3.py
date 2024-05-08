import gdown
import timeit

# Завантаження файлів з Google Drive
url_article1 = 'https://drive.google.com/uc?id=18_R5vEQ3eDuy2VdV3K5Lu-R-B-adxXZh'
url_article2 = 'https://drive.google.com/uc?id=13hSt4JkJc11nckZZz2yoFHYL89a4XkMZ'

gdown.download(url_article1, 'article1.txt', quiet=False)
gdown.download(url_article2, 'article2.txt', quiet=False)

# Зчитування вмісту файлів
with open('article1.txt', 'r', encoding='latin-1') as file:
    article1_text = file.read()

with open('article2.txt', 'r', encoding='latin-1') as file:
    article2_text = file.read()

# Реалізація алгоритму пошуку підрядка Боєра-Мура
def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1

# Реалізація алгоритму пошуку підрядка Кнута-Морріса-Прата
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1

# Реалізація алгоритму пошуку підрядка Рабіна-Карпа
def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string, substring):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)
    
    # Базове число для хешування та модуль
    base = 256 
    modulus = 101  
    
    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    
    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

# Підрядки для пошуку
existing_pattern = "search pattern"
random_pattern = "random pattern"

# Вимірюємо час виконання кожного алгоритму для кожного тексту
for article_num, article_text in enumerate([article1_text, article2_text], start=1):
    print(f"Article {article_num}:")
    print("------------------")
    for pattern_type, pattern in zip(["existing", "random"], [existing_pattern, random_pattern]):
        print(f"Pattern Type: {pattern_type}")
        for algorithm, algorithm_name in zip([boyer_moore_search, kmp_search, rabin_karp_search],
                                              ["Boyer-Moore", "Knuth-Morris-Pratt", "Rabin-Karp"]):
            time_taken = timeit.timeit(lambda: algorithm(article_text, pattern), number=1)
            print(f"{algorithm_name} Time: {time_taken}")
        print("------------------")
    print("------------------")
