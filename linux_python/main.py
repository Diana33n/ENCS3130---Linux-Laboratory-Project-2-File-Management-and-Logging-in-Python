import json
import argparse
import os
class ScriptExecutor:
    def __init__(self, config_file):
        with open(config_file, 'r') as file:
            self.config = json.load(file)
        self.commands = []

    def parse_script(self, script_file):
        with open(script_file, 'r') as file:
            for line in file:
                parts = line.split()
                command_name = parts[0]
                args = parts[1:]
                if command_name == "Mv_last":
                    self.commands.append(MvLast(*args))
                elif command_name == "Categorize":
                    self.commands.append(Categorize(args[0], self.config["Threshold_size"]))
                elif command_name == "Count":
                    self.commands.append(Count(*args))
                elif command_name == "Delete":
                    self.commands.append(Delete(*args))
                elif command_name == "Rename":
                    self.commands.append(Rename(*args))
                elif command_name == "List":
                    self.commands.append(List(*args))
                elif command_name == "Sort":
                    self.commands.append(Sort(*args))

    def execute_commands(self, output_file):
        results = {}
        for command in self.commands:
            result = command.execute()
            results[type(command).__name__] = result

        if self.config["Output"] == "csv":
            with open(output_file, 'w') as file:
                for command, result in results.items():
                    file.write(f"{command},{result}\n")
        else:
            logging.basicConfig(filename=output_file, level=logging.INFO)
            for command, result in results.items():
                logging.info(f"{command}: {result}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script Executor')
    parser.add_argument('-i', '--input', required=True, help='Input script file path')
    parser.add_argument('-o', '--output', required=True, help='Output file path')
    parser.add_argument('-c', '--config', required=True, help='Configuration file path')
    args = parser.parse_args()

    executor = ScriptExecutor(args.config)
    executor.parse_script(args.input)
    executor.execute_commands(args.output)
