from PIL import Image


# Читаем файл с координатами пикселей
keys = []
with open("keys24.txt", "r") as f:
    for line in f:
        line = line.strip()
        if line:
            line = line.replace("(", "").replace(")", "").replace(" ", "")
            x, y = map(int, line.split(","))
            keys.append((x, y))


print("Декодирование текста из синего канала")

# Открываем изображение и переводим в режим RGB
img = Image.open("new24.png").convert('RGB')
pixels = img.load()


bytes_data = []
for x, y in keys:
    r, g, b = pixels[x, y]  
    bytes_data.append(b)     # берем только синий канал

# Преобразуем последовательность байт в строку
text = bytes(bytes_data).decode("utf-8")
print(f"Декодированное сообщение: {text}\n")


print("Кодирование текста в красный канал (метод b1-R, b0-R)")


text_to_encode = input("Введите текст для кодирования: ")
text_bytes = text_to_encode.encode("utf-8")  # Преобразуем в байты UTF-8

# Ограничиваем длину текста: 1 байт = 8 бит = 8 пикселей
max_bytes = len(keys) // 8
if len(text_bytes) > max_bytes:
    text_bytes = text_bytes[:max_bytes]

# Преобразуем байты в биты
bits = []
for byte in text_bytes:
    for i in range(7, -1, -1):
        bits.append((byte >> i) & 1)


if text_bytes:
    first_byte = text_bytes[0]
    first_bits = [(first_byte >> i) & 1 for i in range(7, -1, -1)]
    print(f"\nБиты первого символа: {first_bits}")


print(f"\nИсходные и измененные значения пикселей:")
img2 = Image.open("new24.png").convert('RGB')
pixels2 = img2.load()


# Кодирование
for i, (x, y) in enumerate(keys[:len(bits)]):
    r, g, b = pixels2[x, y]
    old_r = r
    new_r = (r & 0b11111110) | bits[i]  # Меняем только последний бит
    pixels2[x, y] = (new_r, g, b)
    print(f"Пиксель ({x},{y}): {old_r} -> {new_r} (бит={bits[i]})")

img2.save("encoded.png")
print(f"\nСохранено как encoded.png")


print("Проверка: декодирование из красного канала")

# Открываем сохраненное изображение для проверки
img3 = Image.open("encoded.png").convert('RGB')
pixels3 = img3.load()

# Читаем ровно столько битов, сколько записали
decoded_bits = []
for x, y in keys[:len(bits)]:
    r, g, b = pixels3[x, y]
    decoded_bits.append(r & 1) 

# Превращаем биты обратно в байты
decoded_bytes = []
for i in range(0, len(decoded_bits), 8):
    byte = 0
    for j in range(8):
        byte = (byte << 1) | decoded_bits[i + j]
    decoded_bytes.append(byte)

# Преобразуем байты в текст
decoded_text = bytes(decoded_bytes).decode("utf-8")
print(f"Декодированный текст: {decoded_text}")