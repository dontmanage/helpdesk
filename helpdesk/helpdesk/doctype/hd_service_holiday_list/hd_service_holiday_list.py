# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import json

import dontmanage
from dontmanage import _, throw
from dontmanage.model.document import Document
from dontmanage.utils import cint, formatdate, getdate, today


class OverlapError(dontmanage.ValidationError):
    pass


class HDServiceHolidayList(Document):
    def validate(self):
        self.validate_days()
        self.total_holidays = len(self.holidays)

    @dontmanage.whitelist()
    def get_weekly_off_dates(self):
        self.validate_values()
        date_list = self.get_weekly_off_date_list(self.from_date, self.to_date)
        last_idx = max(
            [cint(d.idx) for d in self.get("holidays")]
            or [
                0,
            ]
        )
        for i, d in enumerate(date_list):
            ch = self.append("holidays", {})
            ch.description = _(self.weekly_off)
            ch.holiday_date = d
            ch.weekly_off = 1
            ch.idx = last_idx + i + 1

    def validate_values(self):
        if not self.weekly_off:
            throw(_("Please select weekly off day"))

    def validate_days(self):
        if getdate(self.from_date) > getdate(self.to_date):
            throw(_("To Date cannot be before From Date"))

        for day in self.get("holidays"):
            if not (
                getdate(self.from_date)
                <= getdate(day.holiday_date)
                <= getdate(self.to_date)
            ):
                dontmanage.throw(
                    _("The holiday on {0} is not between From Date and To Date").format(
                        formatdate(day.holiday_date)
                    )
                )

    def get_weekly_off_date_list(self, start_date, end_date):
        start_date, end_date = getdate(start_date), getdate(end_date)

        import calendar
        from datetime import timedelta

        from dateutil import relativedelta

        date_list = []
        existing_date_list = []
        weekday = getattr(calendar, (self.weekly_off).upper())
        reference_date = start_date + relativedelta.relativedelta(weekday=weekday)

        existing_date_list = [
            getdate(holiday.holiday_date) for holiday in self.get("holidays")
        ]

        while reference_date <= end_date:
            if reference_date not in existing_date_list:
                date_list.append(reference_date)
            reference_date += timedelta(days=7)

        return date_list

    @dontmanage.whitelist()
    def clear_table(self):
        self.set("holidays", [])


@dontmanage.whitelist()
def get_events(start, end, filters=None):
    """Returns events for Gantt / Calendar view rendering.

    :param start: Start date-time.
    :param end: End date-time.
    :param filters: Filters (JSON).
    """
    if filters:
        filters = json.loads(filters)
    else:
        filters = []

    if start:
        filters.append(["HD Holiday", "holiday_date", ">", getdate(start)])
    if end:
        filters.append(["HD Holiday", "holiday_date", "<", getdate(end)])

    return dontmanage.get_list(
        "HD Service Holiday List",
        fields=[
            "name",
            "`tabHD Holiday`.holiday_date",
            "`tabHD Holiday`.description",
            "`tabHD Service Holiday List`.color",
        ],
        filters=filters,
        update={"allDay": 1},
    )


def is_holiday(hd_service_holiday_list, date=None):
    """Returns true if the given date is a holiday in the given holiday list"""
    if date is None:
        date = today()
    if hd_service_holiday_list:
        return bool(
            dontmanage.get_all(
                "HD Service Holiday List",
                # flake8: noqa
                dict(name=hd_service_holiday_list, holiday_date=date),
            )
        )
    else:
        return False
