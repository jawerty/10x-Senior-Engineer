# We're gonna input the folder that we want to watch
# everytime there's a file change then get the file change and do our code review
import sys
import time
import os
import argparse
import requests
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from color_logger import CustomFormatter
from prompt import Prompt

logger = logging.getLogger("Senior Engineer")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)

class CustomFileSystemHandler(FileSystemEventHandler):
	def __init__(self, api_url):
		super().__init__()
		self.api_url = api_url
		self.p = Prompt()
		
		self.review_queue = [] # file name and the review and a pass/fail boolean
		
	def print_review(self):
		os.system('cls' if os.name == 'nt' else 'clear')

		pass_reviews = []
		fail_reviews = []
		for review in self.review_queue:
			if review["pass_rating"]:
				pass_reviews.append(review)
			else:
				fail_reviews.append(review)

		logger.debug("Here is your Senior Engineer's Code Review:\n\n")

		if len(pass_reviews) > 0:
			logger.info("--- Files Passed ---\n")
			for review in pass_reviews:
				logger.info("* " + review['file_name'])
				logger.info("CODE REVIEW:\n" + review['review_text'] + "\n")
		
		logger.info("\n")

		if len(fail_reviews) > 0:
			logger.error("--- Files Failed ---\n")
			for review in fail_reviews:
				logger.error("* " + review['file_name'] + "\n")
				logger.error("CODE REVIEW:\n" + review['review_text'] + "\n------------\n\n")


		logger.info("\n\n")

	def on_any_event(self, event):
		event_type = event.event_type
		src_path = event.src_path
		ignore = os.path.isdir(src_path)
		if ignore:
			return

		print("Got file change", src_path)

		with open(src_path, 'r', encoding='utf-8') as f:
			lines = f.readlines()
			file_content = "\n".join(lines)

		file_name = src_path.split('/')[-1]
		prompt = self.p.code_review_prompt(file_content, file_name)

		r = requests.post(self.api_url + "/generate", json={ "prompt": prompt })
		result = r.json()
		pass_check = lambda review: "LGTM" in review


		# deduplicate queue
		for i, review in enumerate(self.review_queue):
			if review["file_name"] == file_name:
				del self.review_queue[i]
				break

		# push to queue
		self.review_queue.append({
			"file_name": file_name,
			"review_text": result['output'],
			"pass_rating": pass_check(result["output"])
		})

		# pop queue if necessary
		if len(self.review_queue) > 10:
			self.review_queue.pop(0)

		self.print_review()

class Watcher:
	def __init__(self, folder):
		self.folder = folder

	def watch(self, event_handler):
		observer = Observer()
		observer.schedule(event_handler, self.folder, recursive=True)
		observer.start()
		return observer


class SeniorEngineer:
	def __init__(self, repository, api_url=None):
		if api_url:
			self.api_url = api_url 

		self.repository = repository

	def run(self):
		watcher = Watcher(self.repository)
		watch_handler = CustomFileSystemHandler(self.api_url)
		observer = watcher.watch(watch_handler)
		os.system('cls' if os.name == 'nt' else 'clear')
		
		print("Running 10x Senior Engineer...")


		try:
			while True:
				time.sleep(1)
		except KeyboardInterrupt:
			observer.stop()

		observer.join()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("repository", help="Pass in the source code folder you want to watch")
	parser.add_argument("--api", help="Link to the colab ngrok url")
	args = parser.parse_args()

	# todo make colab optional and use local llm
	engineer = SeniorEngineer(args.repository, api_url=args.api)
	engineer.run()


	