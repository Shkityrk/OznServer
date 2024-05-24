import os

import pytesseract
from PIL import Image
from django.shortcuts import render

from OznServer import settings
from .forms import ImageUploadForm

# Укажите путь к исполняемому файлу Tesseract
pytesseract.pytesseract.tesseract_cmd = os.path.join(settings.TESSERACT_PATH, 'tesseract.exe')


def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            # Распознавание текста с использованием Tesseract
            image_path = uploaded_image.image.path
            image = Image.open(image_path)
            # Распознание текста с учетом пробелов, табуляций и переносов строк
            text = pytesseract.image_to_string(image, output_type=pytesseract.Output.BYTES, config='--psm 3')
            # Декодирование текста из байтов в строку
            decoded_text = text.decode('utf-8')

            # Фильтрация текста
            lines = []
            for line in decoded_text.split('\n'):
                # Игнорирование строк, начинающихся с символа #
                if not line.strip().startswith('#'):
                    # Исключение строк, содержащих ключевые слова на последнем месте
                    if not (line.strip().endswith('usage') or line.strip().endswith('usages')):
                        # Добавление строки в список строк
                        lines.append(line)
            # Сборка отфильтрованного текста
            filtered_text = '\n'.join(lines)

            return render(request, 'result.html', {'text': filtered_text})
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})
