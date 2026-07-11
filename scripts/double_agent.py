#!/usr/bin/env python3
import os
import sys
import inspect
import argparse
import subprocess
import time

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from main import END_OF_PROMPT, PROMPT_PREFIX

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Start two agents interacting with each others."
    )
    parser.add_argument(
        "--prompt", 
        type=str, 
        default="Hello!",
        help="Initial prompt"
    )
    parser.add_argument(
        "--name_1", 
        type=str,
        default="Agent 1",
        help="Name of the first agent."
    )
    parser.add_argument(
        "--name_2", 
        type=str,
        default="Agent 2",
        help="Name of the second agent."
    )
    parser.add_argument(
        "--system_prompt_1", 
        type=str,
        default="system_prompt.md",
        help="System prompt for the first agent."
    )
    parser.add_argument(
        "--system_prompt_2", 
        type=str,
        default="system_prompt.md",
        help="System prompt for the second agent."
    )
    parser.add_argument(
        "--n_rounds", 
        type=int, 
        default=10, 
        help="Number of discussion rounds."
    )
    return parser.parse_args()


def send_command_and_get_response(process, command, expected_end_marker="> "):
    """
    Sends a command to the CLI agent and reads the response until 
    the prompt marker (e.g., '> ') reappears.
    """
    process.stdin.write(command + "\n" + END_OF_PROMPT + "\n")
    process.stdin.flush()
    
    # Read character by character to detect the prompt
    output = ""
    while True:
        line = process.stdout.readline()
        if not line:
            time.sleep(1)
            continue

        # Check if the agent is waiting for the next input
        if line.startswith(expected_end_marker):
            # Strip the command echo and prompt marker from the returned text
            return output.strip()
        
        output += line


def main():
    args = parse_arguments()
    
    # Start the agent processes
    process_1 = subprocess.Popen(
        ["python3", "./main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        bufsize=0
    )
    process_2 = subprocess.Popen(
        ["python3", "./main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        bufsize=0
    )
    
    # Give the agents a quick second to boot up and consume its initial welcome prompt
    time.sleep(1) 
    
    # Check if the processes died immediately
    if process_1.poll() is not None:
        print(f"Agent process exited early with code: {process.poll()}")
        error_output = process.stdout.read()
        print("--- Agent 1 Error Output ---")
        print(error_output)
        print("----------------------------")
        sys.exit(1)
    if process_2.poll() is not None:
        print(f"Agent process exited early with code: {process.poll()}")
        error_output = process.stdout.read()
        print("--- Agent 2 Error Output ---")
        print(error_output)
        print("----------------------------")
        sys.exit(1)
    
    # Wait for the agents to be ready
    while True:
        line = process_1.stdout.readline()
        if line.startswith(PROMPT_PREFIX):
            break
        else:
            time.sleep(1)
    while True:
        line = process_2.stdout.readline()
        if line.startswith(PROMPT_PREFIX):
            break
        else:
            time.sleep(1)
    
    try:
        if args.system_prompt_1 != "":
            send_command_and_get_response(process_1, f"/system_prompt {args.system_prompt_1}", PROMPT_PREFIX)
        if args.system_prompt_2 != "":
            send_command_and_get_response(process_2, f"/system_prompt {args.system_prompt_2}", PROMPT_PREFIX)
        prompt = args.prompt
        print(f"{args.name_1}: {prompt}\n")
        for r in range(args.n_rounds):
            prompt = send_command_and_get_response(process_2, prompt, PROMPT_PREFIX)
            print(f"{args.name_2}: {prompt}\n")
            prompt = send_command_and_get_response(process_1, prompt, PROMPT_PREFIX)
            print(f"{args.name_1}: {prompt}\n")

    except Exception as e: 
        print(e)
        
    finally:
        # Cleanly close the process
        print("\nClosing agents...")
        process_1.terminate()
        process_2.terminate()
        process_1.wait()
        process_2.wait()


if __name__ == "__main__":
    main()
