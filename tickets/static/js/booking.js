// Этот лог должен появиться первым, как только скрипт начнет выполняться
console.log('booking.js: Скрипт начал выполнение.');

document.addEventListener('DOMContentLoaded', function() {
    console.log('booking.js: DOMContentLoaded сработал. Инициализация обработки мест.');

    try {
        const freeSeatImages = document.querySelectorAll('.seat-visual');
        console.log('booking.js: Найдено изображений свободных мест (.seat-visual):', freeSeatImages.length);

        if (freeSeatImages.length === 0) {
            console.warn('booking.js: Внимание! Не найдено элементов с классом "seat-visual". Проверьте HTML.');
        }

        freeSeatImages.forEach(function(img) {
            img.addEventListener('click', function() {
                try {
                    // Получаем row и seat из data-атрибутов изображения
                    const row = this.dataset.row;
                    const seat = this.dataset.seat;
                    const seatId = `${row}-${seat}`; // Формируем seat_id здесь!

                    console.log('booking.js: Клик по изображению места. row:', row, 'seat:', seat, 'seatId:', seatId);

                    const checkbox = this.previousElementSibling;
                    console.log('booking.js: Найден previousElementSibling:', checkbox);

                    if (checkbox && checkbox.tagName === 'INPUT' && checkbox.type === 'checkbox' && checkbox.classList.contains('seat-checkbox')) {
                        console.log('booking.js: Элемент подтвержден как чекбокс.');
                        console.log('booking.js: Состояние чекбокса ДО клика:', checkbox.checked);

                        checkbox.checked = !checkbox.checked; // Переключение состояния

                        // ПРИСВАИВАЕМ VALUE ЧЕКБОКСУ ЗДЕСЬ!
                        checkbox.value = seatId;
                        console.log('booking.js: Чекбокс value установлен на:', checkbox.value);

                        console.log('booking.js: Состояние чекбокса ПОСЛЕ клика:', checkbox.checked);

                        if (checkbox.checked) {
                            this.classList.add('selected');
                            console.log('booking.js: Класс "selected" добавлен.');
                        } else {
                            this.classList.remove('selected');
                            console.log('booking.js: Класс "selected" удален.');
                            checkbox.value = ""; // Если снимаем выбор, можно очистить value, чтобы не отправлялся
                        }
                    } else {
                        console.error('booking.js: ОШИБКА: Чекбокс не найден или не соответствует ожидаемому.');
                    }
                } catch (clickError) {
                    console.error('booking.js: Ошибка при обработке клика:', clickError);
                }
            });
        });

        // Этот блок отвечает за визуальное выделение мест, которые уже выбраны
        // (например, если пользователь вернулся на страницу бронирования)
        // Здесь мы полагаемся на то, что бэкенд все еще заполняет 'checked' атрибут, если это "ваше" место.
        document.querySelectorAll('.seat-checkbox').forEach(function(checkbox) {
            if (checkbox.checked) {
                const nextImg = checkbox.nextElementSibling;
                if (nextImg && nextImg.classList.contains('seat-visual')) {
                    nextImg.classList.add('selected');
                }
            }
        });

    } catch (domLoadError) {
        console.error('booking.js: Ошибка при инициализации DOMContentLoaded:', domLoadError);
    }
});

console.log('booking.js: Конец файла.');