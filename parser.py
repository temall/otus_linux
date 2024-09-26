import subprocess
from subprocess import run
import datetime
import io


def parser():
    result = run(["ps", "aux"], capture_output=True, text=True)
    output = result.stdout
    lines = output.split("\n")
    users = set()
    summary_processes = len(lines) - 1
    user_processes = {}
    current_time = datetime.datetime.now()
    result_file = current_time.strftime("%d-%m-%Y-%H.%M-scan.txt")

    summary_cpu_usage = 0
    summary_mem_usage = 0
    max_process_cpu_usage = 0
    max_process_mem_usage = 0
    max_process_cpu_name = ""
    max_process_mem_name = ""
    for line in lines[1:-1]:
        field = line.split()
        user = field[0]
        users.add(user)
        cpu_usage = float(field[2])
        mem_usage = float(field[3])
        summary_cpu_usage += cpu_usage
        summary_mem_usage += mem_usage
        command = " ".join(field[10:])[:20]
        user_processes[user] = user_processes.get(user, 0) + 1
        if cpu_usage > max_process_cpu_usage:
            max_process_cpu_usage = cpu_usage
            max_process_cpu_name = command
        if mem_usage > max_process_mem_usage:
            max_process_mem_usage = mem_usage
            max_process_mem_name = command

    result = f"Отчет о состоянии системы:\n"
    result += f"Пользователи системы: {', '.join(users)}\n"
    result += f"Процессов запущено: {summary_processes}\n"
    result += f"Пользовательских процессов:\n"
    for user, proc in user_processes.items():
        result += f"{user}: {proc}\n"
    result += f"Всего памяти используется: {summary_mem_usage:.1f}%\n"
    result += f"Всего CPU используется: {summary_cpu_usage:.1f}%\n"
    result += f"Больше всего памяти использует: {max_process_mem_name}\n"
    result += f"Больше всего CPU использует: {max_process_cpu_name}\n"

    print(result)

    with open(result_file, "w") as file:
        file.write(result)


if __name__ == '__main__':
    parser()
