import argparse
import os
import sys
from collections import Counter
from json import dump, dumps


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=dir_path)
    args = parser.parse_args()
    return args.path


def dir_path(path):
    if os.path.isdir(path):
        return path


def main():
    path = parse_arguments()
    log_list = collect_logs(path)
    log_file(log_list, path)


def collect_logs(path):
    log_list = []
    files_list = os.listdir(path)
    for file in files_list:
        if ".log" in file:
            log_list.append(file)
    if not log_list:
        sys.exit('There are not any log files. Check correct path and try again')
    return log_list


def log_file(log_list, path):
    for log in log_list:
        json_data = parse_data_to_dict(path, log)
        output_file = log.replace(".log", ".json")
        with open(output_file, "w") as json_file:
            dump(json_data, json_file, indent=4)
            print(f"Statistics for {log_file}:")
            print(dumps(json_data, indent=4))


def parse_data_to_dict(path, log):
    lines = 0
    method_counter = Counter()
    ip_counter = Counter()
    longest_requests = []
    durations = []
    os.chdir(path)
    with open(log, "r") as f:
        for line in f:
            lines += 1
            item = line.split()
            method = item[5][1:]
            method_counter[method] += 1
            ip = item[0]
            ip_counter[ip] += 1
            duration = int(item[-1].replace('"', ""))
            date = item[3][1:] + " " + item[4][:-1]
            url = item[10].replace('"', '')
            durations.append(duration)
    sorted_durations = sorted(durations, reverse=True)
    for dur in sorted_durations:
        d = {
            "ip": ip,
            "date": date,
            "method": method,
            "url": url,
            "duration": dur
        }
        longest_requests.append(d)

    top_ips = dict(ip_counter.most_common(3))
    total_stat = dict(method_counter)

    return {
        "top_ips": top_ips,
        "top_longest": longest_requests[:3],
        "total_stat": total_stat,
        "total_requests": lines,
    }


if __name__ == "__main__":
    main()
