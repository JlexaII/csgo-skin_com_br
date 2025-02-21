import re

# Пути к файлам
html_file = "index.html"
css_file = "style.css"
cleaned_css_file = "cleaned_style.css"

# Читаем HTML и собираем используемые классы и ID
with open(html_file, "r", encoding="utf-8") as f:
    html_content = f.read()

used_classes = set(re.findall(r'class="(.*?)"', html_content))
used_ids = set(re.findall(r'id="(.*?)"', html_content))

# Разбиваем строки с классами (если там несколько через пробел)
used_classes = {cls for group in used_classes for cls in group.split()}
used_ids = {id_ for id_ in used_ids}

# Читаем CSS
with open(css_file, "r", encoding="utf-8") as f:
    css_lines = f.readlines()

# Фильтруем CSS, оставляя только используемые классы и ID
cleaned_css = []
keep = False

for line in css_lines:
    # Проверяем, содержит ли строка селектор класса или ID
    match = re.match(r'(\.|#)([a-zA-Z0-9_-]+)\s*\{?', line)
    
    if match:
        selector_type, selector_name = match.groups()
        
        # Проверяем, используется ли этот селектор
        if (selector_type == "." and selector_name in used_classes) or \
           (selector_type == "#" and selector_name in used_ids):
            keep = True
        else:
            keep = False
    
    if keep or line.strip() == "}":  # Сохраняем строки, пока стиль не закроется
        cleaned_css.append(line)

# Записываем новый CSS-файл
with open(cleaned_css_file, "w", encoding="utf-8") as f:
    f.writelines(cleaned_css)

print(f"✅ Готово! Очищенный CSS сохранён в {cleaned_css_file}")
