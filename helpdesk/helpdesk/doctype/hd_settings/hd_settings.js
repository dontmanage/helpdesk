// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on("HD Settings", {
  refresh: function (frm) {
    frm.add_custom_button(__("Regenerate Search Index"), () => {
      dontmanage.call({
        method: "helpdesk.search.build_index",
        callback: function (r) {
          dontmanage.msgprint(__("Search Index Regenerated"));
        },
      });
    });
  },
});
