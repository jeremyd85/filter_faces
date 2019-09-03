from recognize import RecognizeFaces
import os
import csv
import re
import datetime

def sign_in_csv(process_frame_count=2, sign_in_dir=""):
    sign_in_path = get_sign_in_path(sign_in_dir)
    with open(sign_in_path) as csv_file:
        r = RecognizeFaces(frame_count=process_frame_count)


def get_sign_in_path(sign_in_dir):
    if not os.path.exists(sign_in_dir):
        os.makedirs(sign_in_dir)

    sign_ins = os.listdir(sign_in_dir)
    now = datetime.datetime.now()
    cur_date = now.strftime('%Y-%m-%d')
    for s in sign_ins:
        match = re.match(r"(\d-\d-\d)(\.csv)", s)
        if match and cur_date == match.group(1):
            return os.path.join(sign_in_dir, s)

    sign_in_path = os.path.join(sign_in_dir, "{0}.csv".format(cur_date))
    with open(sign_in_path, "w") as csv_file:
        return sign_in_path