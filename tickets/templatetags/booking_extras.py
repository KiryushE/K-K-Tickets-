from django import template

register = template.Library()


@register.filter
def get_row_bookings(bookings, row):
    # Возвращает список бронирований только для указанного ряда
    return [b for b in bookings if b.row == row]


@register.filter
def get_seat_from_list(row_bookings, seat):
    # Возвращает конкретное бронирование из списка для ряда
    for b in row_bookings:
        if b.seat == seat:
            return b
    return None