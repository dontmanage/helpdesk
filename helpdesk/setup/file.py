import dontmanage


def create_helpdesk_folder():
    f = dontmanage.new_doc("File")
    f.file_name = "Helpdesk"
    f.is_folder = 1
    f.folder = "Home"
    f.insert(ignore_if_duplicate=True)
