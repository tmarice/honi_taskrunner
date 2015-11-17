import argparse
import zipfile
import os


class TaskManager(object):
    """ Manage the task list and taks operations.
    """

    CONFIG_BASE_DIR = '/usr/share/honi_taskmanager/'
    CONFIG_TASKS_DIR = os.path.join(CONFIG_BASE_DIR, 'tasks')

    def __init__(self):
        pass

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
        archive.extractall(TaskManager.CONFIG_TASKS_DIR)

    def run(self, filename):
        """ Run the task with input data found in the test directories.
        """
        tests_dir = os.path.join(TaskManager.CONFIG_TASKS_DIR, filename)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("action", metavar="ACTION", help="action to be taken: add or run", dest="action")
    parser.add_argument("name", metavar="NAME", help="name of the file to be added or task to be run", dest="name")

    options = parser.parse_args()
    task_manager = TaskManager()

    if options.action == "add":
        task_manager.add(options.name)
    elif options.action == "run":
        task_manager.run(options.name)

