# import HtmlTestRunner
from unittest import defaultTestLoader,TextTestRunner

start_dir = "module-test/"
discover = defaultTestLoader.discover(start_dir = start_dir, pattern = r'*_test.py')
if __name__ == "__main__":
    with open("report.html",'w+') as f:
        runner = TextTestRunner(stream=f, verbosity = 2)
        runner.run(discover)