from recognize import RecognizeFaces
import os
import csv
import re
import datetime



class SigninRecognizer(RecognizeFaces):

    def __init__(self, recognizers=[], scale=0.4, frame_count=5, sign_in=False, file_path=""):
        super().__init__(recognizers, scale, frame_count, sign_in)
        self.file_path = file_path
        self.sign_in_path = self.get_sign_in_path()
        self.members_present = self._get_members()

    def _get_members(self):
        with open(self.sign_in_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            return [r[0] for r in csv_reader]

    def sign_in_csv(self, email):
        if email in self.members_present:
            return True
        else:
            with open(self.sign_in_path, "a+") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([str(email), True])
            self.members_present = self._get_members()
            return True

    def get_sign_in_path(self):
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)

        sign_ins = os.listdir(self.file_path)
        now = datetime.datetime.now()
        cur_date = now.strftime('%Y-%m-%d')
        for s in sign_ins:
            match = re.match(r"(\d-\d-\d)(\.csv)", s)
            if match and cur_date == match.group(1):
                return os.path.join(self.file_path, s)

        sign_in_path = os.path.join(self.file_path, "{0}.csv".format(cur_date))
        with open(sign_in_path, "w") as csv_file:
            return sign_in_path

    def green_condition(self, name):
        if name not in self.members_present:
            self.sign_in_csv(name)
            return False
        else:
            return True


def sign_in(process_frame_count=2, sign_in_dir=""):
    r = SigninRecognizer(frame_count=process_frame_count, file_path=sign_in_dir)
    r.setup()
    r.start_window()

