# linux.py
#=====================================================
import argparse
import json
import logging
import os
from commands import mv_last, categorize, count_files, delete_file, rename_file, list_files, sort_files

#=====================================================

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config
#=====================================================

def execute_script(script_path, config, log_output):
    commands = {
        'mv_last': mv_last,
        'categorize': categorize,
        'count_files': count_files,
        'delete_file': delete_file,
        'rename_file': rename_file,
        'list_files': list_files,
        'sort_files': sort_files
    }

    with open(script_path, 'r', encoding='utf-8') as f:
        script_lines = f.readlines()

    results = []
    for line in script_lines:
        if not line.strip():
            continue

        parts = line.strip().split()
        if len(parts) < 1:
            continue

        command_name = parts[0]
        args = parts[1:]

        if command_name in commands:
            command = commands[command_name]
            if command_name == 'categorize':
                if len(args) == 1:
                    args.append(config['Threshold_size'])
                elif len(args) == 2:
                    pass
                else:
                    results.append((line.strip(), 'FAILURE'))
                    continue
            result = command(*args)
            results.append((line.strip(), 'SUCCESS' if result is None else result))
        else:
            results.append((line.strip(), 'FAILURE'))

    output_results(results, log_output, config['Output'], config['Same_dir'])
#=====================================================

def output_results(results, log_output, output_format, same_dir):
    if not log_output:
        raise ValueError("Output log file path is empty")

    log_dir = os.path.dirname(log_output)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if output_format == 'log':
        import csv
        csv_path = log_output.replace('.log', '.csv')
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Command', 'Result'])
            for result in results:
                writer.writerow(result)
        logging.info(f"Results written to {csv_path}")
    else:
        with open(log_output, 'w', encoding='utf-8') as f:
            for result in results:
                f.write(f"{result[0]}: {result[1]}\n")
        logging.info(f"Results written to {log_output}")
#=====================================================

def setup_logging(log_dir, max_log_files):
    if not log_dir:
        log_dir = "logs"  # Default to a 'logs' directory if log_dir is empty
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_files = [os.path.join(log_dir, f) for f in os.listdir(log_dir) if f.endswith('.log')]
    log_files.sort(key=os.path.getmtime)

    while len(log_files) >= max_log_files:
        oldest_log = log_files.pop(0)
        os.remove(oldest_log)
        logging.info(f"Removed old log file: {oldest_log}")

    logging.basicConfig(filename=os.path.join(log_dir, 'execution.log'), level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', encoding='utf-8')
#=====================================================

def main():
    parser = argparse.ArgumentParser(description='Script Executor')
    parser.add_argument('-i', '--input', required=True, help='Input script file')
    parser.add_argument('-o', '--output', required=True, help='Output log file')
    parser.add_argument('-c', '--config', default='my_file.json', help='Configuration file')
    args = parser.parse_args()

    config = load_config(args.config)
    setup_logging(os.path.dirname(args.output), config['Max_log_files'])

    execute_script(args.input, config, args.output)
#=====================================================

if __name__ == '__main__':
    main()
