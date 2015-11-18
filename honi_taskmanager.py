#!/usr/bin/env python

import argparse
import zipfile
import os

import yaml
import subprocess32 as subprocess
from natsort import natsorted

class Settings(object):
    CONFIG_BASE_DIR = '/mnt/data/honi_taskmanager/'
    CONFIG_TASKS_DIR = os.path.join(CONFIG_BASE_DIR, 'tasks')


class TaskManager(object):
    """ Manage the task list and taks operations.
    """

    CONFIG_FILENAME = '/etc/honi_taskmanager.yaml'

    def __init__(self):
        self._load_settings(Settings.__dict__, TaskManager.CONFIG_FILENAME)
        self._verify_dir(Settings.CONFIG_BASE_DIR)
        self._verify_dir(Settings.CONFIG_TASKS_DIR)

    def _load_settings(self, config, config_filename):
        with open(config_filename, 'r') as config_file:
            config.update(yaml.load(config_file))

    def _verify_dir(self, dirname):
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def add(self, filename):
        """ Add test data from the input file.

        The method unzips the archive with the following data structure:
        test.zip
            /task1
                /task1.in.1
                /task1.in.2
                ...
                /task1.out.1
                /task1.out.2
                ...
            /task2
                ...
        
        Args:
            filename (str): name of the zip file with the test data
        """
        archive = zipfile.ZipFile(filename, 'r')
        archive.extractall(Settings.CONFIG_TASKS_DIR)

    def run(self, filename):
        """ Run the task with input data found in the test directories.

        The test folder contains a number of dummy inputs, of format
        <task_name>.dummy.in.X, with coresponding <task_name>.dummy.out.X outputs.
        Afterwards the real inputs are of format <task_name>.in.X, and
        corresponding output <task_name>.out.X.
        """
        tests_dir = os.path.join(Settings.CONFIG_TASKS_DIR, os.path.basename(filename))
        files = os.listdir(tests_dir)

        dummy_ins = [f for f in files if 'dummy.in.' in f]
        dummy_outs = [f for f in files if 'dummy.out.' in f]
        real_ins = [f for f in files if '.in.' in f and f not in dummy_ins]
        real_outs = [f for f in files if '.out.' in f and f not in dummy_outs]

        dummy_tests = zip(natsorted(dummy_ins), natsorted(dummy_outs))
        real_tests = zip(natsorted(real_ins), natsorted(real_outs))

        exec_filename = "./{0}".format(filename)

        print "========== DUMMY TESTS ==========="

        for test_in, test_out in dummy_tests:
            status = "FAIL"
            with open(os.path.join(tests_dir, test_in), 'r') as test_in_file:
                try:
                    output = subprocess.check_output(exec_filename, stdin=test_in_file, timeout=1)
                except subprocess.TimeoutExpired:
                    status = "TIMEOUT"
                if self.check_output(output, os.path.join(tests_dir, test_out)):
                    status = "OK"
            print "{0}: {1}".format(test_in, status)

        print
        print "========== REAL TESTS ==========="

        for test_in, test_out in real_tests:
            status = "FAIL"
            with open(os.path.join(tests_dir, test_in), 'r') as test_in_file:
                try:
                    output = subprocess.check_output(exec_filename, stdin=test_in_file, timeout=1)
                except subprocess.TimeoutExpired:
                    status = "TIMEOUT"
                if self.check_output(output, os.path.join(tests_dir, test_out)):
                    status = "OK"
            print "{0}: {1}".format(test_in, status)

    def check_output(self, output, correct_filename):
        with open(correct_filename, 'r') as correct_file:
            correct_output = correct_file.read()
            if correct_output.strip() == output.strip():
                return True
            return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("action", metavar="ACTION", help="action to be taken: add or run")
    parser.add_argument("name", metavar="NAME", help="name of the file to be added or task to be run")

    options = parser.parse_args()
    task_manager = TaskManager()

    if options.action == "add":
        task_manager.add(options.name)
    elif options.action == "run":
        task_manager.run(options.name)
