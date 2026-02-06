.PHONY: clean

clean:
	rm -rf __pycache__
	rm -rf functions/__pycache__
	rm -f .chat.history
	rm -f .function_calls.log
	rm -f .prompt_history
	rm -f log.txt
	rm -rf test/*
