from HtmlTestRunner import HTMLTestRunner as TextTestRunner
from unittest import defaultTestLoader
# from unittest import TextTestRunner

start_dir = "module-test/"
discover = defaultTestLoader.discover(start_dir = start_dir, pattern = r'*_test.py')
if __name__ == "__main__":
    runner = TextTestRunner(report_name = "PKUReader_backend_Test_Report", combine_reports = True)
    runner.run(discover)