.PHONY: clean

clean:
	rm -rf __pycache__
	rm -rf functions/__pycache__
	rm -f .chat.history
	rm -f .prompt_history
	rm -f log.txt
	rm -f test/log.txt
	cd test/html_renderer && cargo clean && rm -f Cargo.lock && rm -f log.txt
