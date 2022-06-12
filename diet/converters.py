from datetime import date


class DateConverter:
    regex = '\d\d\d\d-\d\d\-\d\d'

    def to_python(self, value):
        year, day, month = value.split('-')
        return date(int(year), int(day), int(month))

    def to_url(self, value):
        return value
