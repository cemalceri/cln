# calendarapp/utils.py
from calendar import HTMLCalendar

from django.core.management import BaseCommand, CommandError

from calendarapp.models.concrete.etkinlik import EtkinlikModel


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        events_per_day = events.filter(start_time__day=day)
        d = ""
        for event in events_per_day:
            d += f"<li> {event.get_html_url} </li>"
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return "<td></td>"

    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ""
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f"<tr> {week} </tr>"

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        events = EtkinlikModel.objects.filter(
            start_time__year=self.year, start_time__month=self.month
        )
        cal = (
            '<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        )  # noqa
        cal += (
            f"{self.formatmonthname(self.year, self.month, withyear=withyear)}\n"
        )  # noqa
        cal += f"{self.formatweekheader()}\n"
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f"{self.formatweek(week, events)}\n"
        return cal


def get_verbose_name(model, field):
    return model._meta.get_field(field).verbose_name


def formErrorsToText(Errors, instance):
    errorText = ""
    for field in Errors.get_json_data():
        if Errors.get_json_data()[field][0]["code"] == "required":
            errorText += get_verbose_name(instance, field) + " alanı boş bırakılamaz.<br>"
        else:
            errorText += get_verbose_name(instance, field) + ": " + Errors.get_json_data()[field][0][
                "message"] + "<br>"
    return errorText


def gun_adi_ve_saati_getir(tarih):
    gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    gun = gunler[tarih.weekday()]
    saat = tarih.strftime("%H:%M")
    return "-" + gun + " " + saat + "-"
