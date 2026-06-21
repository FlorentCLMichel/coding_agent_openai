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
        description="Summarize long documents using an interactive CLI AI agent."
    )
    parser.add_argument(
        "doc_path", 
        type=str, 
        help="Path to the document text file to summarize."
    )
    parser.add_argument(
        "--max_doc_len", 
        type=int, 
        default=2000, 
        help="Maximum number of words per document chunk (default: 2000)."
    )
    parser.add_argument(
        "--max_summary_len", 
        type=int, 
        default=1000, 
        help="Maximum number of words in the intermediate summary before triggering a compression step (default: 1000)."
    )
    return parser.parse_args()

def split_document(text, max_words):
    """Splits text into chunks of at most max_words."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk_words = words[i:i + max_words]
        chunks.append(" ".join(chunk_words))
    return chunks

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
    
    if not os.path.exists(args.doc_path):
        print(f"Error: File not found at {args.doc_path}")
        sys.exit(1)
        
    with open(args.doc_path, "r", encoding="utf-8") as f:
        document_text = f.read()
        
    chunks = split_document(document_text, args.max_doc_len)
    print(f"Split document into {len(chunks)} chunks.")

    # Start the agent process 
    # Adjust 'bufsize=0' and 'universal_newlines=True' (text mode) for seamless communication
    process = subprocess.Popen(
        ["python3", "./main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        bufsize=0
    )
    
    # Give the agent a quick second to boot up and consume its initial welcome prompt
    time.sleep(1) 
    
    # Check if the process died immediately
    if process.poll() is not None:
        print(f"Agent process exited early with code: {process.poll()}")
        # Read whatever error it printed
        error_output = process.stdout.read()
        print("--- Agent Error Output ---")
        print(error_output)
        print("--------------------------")
        sys.exit(1)
    
    summary = ""
    
    # Wait for the agent to be ready
    while True:
        line = process.stdout.readline()
        if line.startswith(PROMPT_PREFIX):
            break
        else:
            time.sleep(1)
    
    try:
        for idx, chunk in enumerate(chunks):
            print(f"\n--- Processing Chunk {idx + 1}/{len(chunks)} ---")
            
            # Count words in current summary
            summary_word_count = len(summary.split())
            
            if idx == 0:
                # First chunk: Just ask for an initial summary
                prompt = f"Please summarize the following text:\n\n{chunk}"
                print("Sending initial chunk...")
                summary = send_command_and_get_response(process, prompt, PROMPT_PREFIX)
                
            else:
                # Reset context for the next iteration
                print("Resetting agent context...")
                send_command_and_get_response(process, "/reset_context", PROMPT_PREFIX)
                
                # If current summary is getting too long, compress it first
                if summary_word_count > args.max_summary_len:
                    print(f"Summary length ({summary_word_count} words) exceeds max. Compressing...")
                    compress_prompt = f"Please condense and summarize this text to make it shorter:\n\n{summary}"
                    summary = send_command_and_get_response(process, compress_prompt, PROMPT_PREFIX)
                    
                    # Reset context again after compressing to keep things clean
                    send_command_and_get_response(process, "/reset", PROMPT_PREFIX)
                
                # Feed the working summary + the next chunk to the model
                prompt = (
                    f"Here is the summary of the document so far:\n\n{summary}\n\n"
                    f"Here is the next part of the document:\n\n{chunk}\n\n"
                    f"Please update the summary to include the relevant points from the new text. The new summary should be self-contained and understandable independently of the previous one."
                )
                print("Sending working summary + next chunk...")
                summary = send_command_and_get_response(process, prompt, PROMPT_PREFIX)

        print("\n================ FINAL SUMMARY ================")
        print(summary)
        print("===============================================")
        
    finally:
        # Cleanly close the process
        print("\nClosing agent...")
        process.terminate()
        process.wait()

if __name__ == "__main__":
    main()
