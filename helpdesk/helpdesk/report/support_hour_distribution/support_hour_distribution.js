// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt
/* eslint-disable */

dontmanage.query_reports["Support Hour Distribution"] = {
  filters: [
    {
      lable: __("From Date"),
      fieldname: "from_date",
      fieldtype: "Date",
      default: dontmanage.datetime.nowdate(),
      reqd: 1,
    },
    {
      lable: __("To Date"),
      fieldname: "to_date",
      fieldtype: "Date",
      default: dontmanage.datetime.nowdate(),
      reqd: 1,
    },
  ],
};
