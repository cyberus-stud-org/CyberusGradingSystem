import threading
import thm
import queuedb
import config


class THMGradingSystem:

    def __init__(self):

        self.driver = thm.start_driver()
        self.queue = queuedb.Queuedb(config.DB_FILE_NAME)
        self.run()

    def queue_entry(self, data_list: list):
        """Adds an entry to the queuedb if it's unique and return True on success and False otherwise"""
        # check if entry exists in the db
        if not self.queue.check_existence(data_list):
            # add the entry do the db
            self.queue.push(data_list)
            return True
        return False

    def check_driver_status(self):
        """Check the state of the driver and returns True if 'on' and False if 'off'"""
        # checks if the driver is working
        with open(config.DRIVER_STATUS_FILE) as f:
            lines = f.readlines()
            if lines[0] == 'on':
                return True
            elif lines[0] == 'off':
                return False

    def change_driver_status(self, state):
        """Change the state of the driver in the status file"""
        # change driver status in status file
        with open(config.DRIVER_STATUS_FILE, 'w') as f:
            f.write(state)

    def run(self):
        """Running the whole THM Grading System"""
        # run THM Grading System every known interval of time
        threading.Timer(config.THM_GRADING_SYSTEM_TIMER, self.run).start()
        # run if the driver is off (sleeping)
        if self.check_driver_status() is False:
            # set the driver's state to on
            self.change_driver_status('on')
            while self.queue.size() > 0:
                # get the first element of the queue
                front = self.queue.front()
                # create THM profile object
                thm_profile = thm.THMProfile(self.driver, front[0])

                ###################################
                # send a request to the db endpoint
                # To be added
                ###################################

                print(front, thm_profile.check_if_room_completed(front[1]) or thm_profile.check_if_room_completed(front[1]))
                # remove the element from the queue after finishing
                self.queue.pop(front)
            # set the state of the driver back to off after finishing
            self.change_driver_status('off')
