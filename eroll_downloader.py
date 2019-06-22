
import pandas as pd
import requests
import os
import errno
import csv

file = 'ac_code_and_parts.csv'


def read_csv_file(name, skip_header=True):
    with open(name) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        if skip_header:
            return list(reader)[1:]
        else:
            return list(reader)


code_map = {}
part_map = {}
vs_list = []


def code_mapper(file):
    vidhansabhas = read_csv_file(file)

    for vs in vidhansabhas:
        code_map.update({vs[1]: vs[0]})
        part_map.update({vs[1]: vs[2]})
        vs_list.append(vs[1])

    return code_map, part_map, vs_list


def eroll_downloader(code_map=code_map, part_map=part_map, vs_list=vs_list):

    ac_name = str.title(input('Enter Vidhansabha name: '))

    while ac_name in vs_list:
        ac_code = code_map.get(ac_name)
        parts = int(part_map.get(ac_name))
        i = int(input('Enter start: '))

        part_list = ["%04d" % x for x in range(i, parts+1)]

        for part in part_list:
            url = 'http://164.100.150.3/mrollpdf1/ceopdf/MR0{}/MR0{}{}.pdf'.format(
                ac_code, ac_code, part)
            print(url)

            response = requests.get(url, allow_redirects=False)
            filename = '/Users/escapist21/Downloads/erolls/{}/{}.pdf'.format(
                ac_name, i)

            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise

            handle = open(filename, 'wb')
            i += 1
            for chunk in response.iter_content(chunk_size=512):
                if chunk:
                    handle.write(chunk)
                else:
                    print('the task is completed')

        print('Operation successfully completed')

    else:
        print('Vidhansabha name not found')
        eroll_downloader()


def main():
    code_mapper(file)
    eroll_downloader(code_map, part_map, vs_list)


if __name__ == '__main__':
    main()
