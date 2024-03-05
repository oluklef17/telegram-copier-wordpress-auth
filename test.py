import subprocess

command = "your_command_here"
input_data = "your_input_here"

subprocess.run(command, input=input_data.encode(), text=True)
