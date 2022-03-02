import shutil

class Database:
    def __init__(self, db_from_fp, meta_from_fp, date, dest):
        self.db_fp = str(dest / db_from_fp.name)
        self.meta_fp = str(dest / meta_from_fp.name)
        self.date_downloaded = date.strftime('%Y-%m-%d')
        self.copy_db(db_from_fp, meta_from_fp, dest)

    def get_db_path(self):
        print("DB path is {0}".format(self.db_fp))

    def get_meta_path(self):
        print("Meta path is {0}".format(self.meta_fp))

    def get_date(self):
        print("Date is {0}".format(self.date_downloaded))

    def copy_db(self, db_from_fp, meta_from_fp, dest):
        #also change the timestamps?
        shutil.copy2(db_from_fp, dest)
        shutil.copy2(meta_from_fp, dest)