# Copyright (c) 2013, DontManage and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import dontmanage


def execute(filters=None):
    columns = [
        {
            "fieldname": "creation_date",
            "label": "Date",
            "fieldtype": "Date",
            "width": 300,
        },
        {
            "fieldname": "first_response_time",
            "fieldtype": "Duration",
            "label": "First Response Time",
            "width": 300,
        },
    ]

    data = dontmanage.db.sql(
        """
		SELECT
			date(creation) as creation_date,
			avg(first_response_time) as avg_response_time
		FROM `tabHD Ticket`
		WHERE
			date(creation) between %s and %s
			and first_response_time > 0
		GROUP BY creation_date
		ORDER BY creation_date desc
	""",
        (filters.from_date, filters.to_date),
    )

    return columns, data
