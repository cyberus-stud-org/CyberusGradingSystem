from selenium import webdriver
import selenium.common.exceptions
from bs4 import BeautifulSoup
from time import sleep
import os

import config


def start_driver():
    # starts chrome driver with specific options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    return webdriver.Chrome()


class THMProfile:

    def __init__(self, driver, username):

        # set the driver
        self.driver = driver
        # check if the browser is open
        try:
            # go to THM user's profile
            self.driver.get(config.THM_PROFILE_URL + username)
        except selenium.common.exceptions.WebDriverException:
            self.driver = start_driver()
            sleep(1)
            self.driver.get(config.THM_PROFILE_URL + username)
        # check if THM blocked our requests
        requests_blocked = self.check_if_requests_blocked()
        # deal with the block
        time_to_sleep = 2
        while requests_blocked:
            sleep(time_to_sleep)
            self.driver.close()
            sleep(time_to_sleep)
            self.driver = start_driver()
            self.driver.get(config.THM_PROFILE_URL + username)
            time_to_sleep += 1
            requests_blocked = self.check_if_requests_blocked()

        # check if username exists
        self.username_exists = self.check_username_existence()

        if self.username_exists:
            # get number of completed rooms
            try:
                number_of_completed_rooms = self.get_number_of_completed_rooms()
            except Exception:
                sleep(3)
                number_of_completed_rooms = self.get_number_of_completed_rooms()

            # get number of current shown rooms
            number_of_current_shown_rooms = self.get_number_of_current_shown_rooms()

            # show more rooms while the number of current shown rooms is less than the actual completed rooms
            while number_of_current_shown_rooms < number_of_completed_rooms:
                self.show_more_rooms()
                number_of_current_shown_rooms = self.get_number_of_current_shown_rooms()

    def get_number_of_completed_rooms(self):
        """:returns the number of completed rooms"""
        return int(BeautifulSoup(self.driver.page_source, features='html.parser').find('div', {'id': 'rooms-completed'}).text)

    def get_number_of_current_shown_rooms(self):
        """:returns the number of currently shown rooms"""
        soup = BeautifulSoup(self.driver.page_source, features='html.parser')
        return len(soup.find_all('div', {'class': 'room-card-design-title'}))

    def show_more_rooms(self):
        """get more rooms with JS function"""
        self.driver.execute_script('completedRoomsAdd()')

    def get_all_completed_rooms(self):
        """:returns the name of all completed rooms"""
        soup = BeautifulSoup(self.driver.page_source, features='html.parser')
        return [room_name.text for room_name in soup.find_all('div', {'class': 'room-card-design-title'})]

    def check_if_room_completed(self, room_name):
        """:returns True if the user completed the room, otherwise it will return false"""
        all_completed_rooms = self.get_all_completed_rooms()
        # loops through all completed rooms
        for room in all_completed_rooms:
            # check if the room name matches the wanted room
            if room_name == room.strip() or room_name in room.strip():
                return True
        return False

    def check_if_requests_blocked(self):
        """:returns True if THM blocked our requests"""
        if 'What can I do to prevent this in the future?' in self.driver.page_source:
            return True
        return False

    def check_username_existence(self):
        """:returns True if username exists, otherwise if will return False"""
        if 'Uh-oh, this page has been lost in the matrix.' in self.driver.page_source:
            return False
        return True
