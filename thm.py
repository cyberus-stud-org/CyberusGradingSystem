from bs4 import BeautifulSoup
from time import sleep

import config


class THMProfile:

    def __init__(self, driver, username):

        # set the driver
        self.driver = driver
        # go to THM user's profile
        self.driver.get(config.THM_PROFILE_URL + username)

        # get number of completed rooms
        try:
            number_of_completed_rooms = self.get_number_of_completed_rooms(self.driver.page_source)
        except Exception:
            sleep(3)
            number_of_completed_rooms = self.get_number_of_completed_rooms(self.driver.page_source)

        # get number of current shown rooms
        number_of_current_shown_rooms = self.get_number_of_current_shown_rooms()

        # show more rooms while the number of current shown rooms is less than the actual completed rooms
        while number_of_current_shown_rooms < number_of_completed_rooms:
            self.show_more_rooms()
            number_of_current_shown_rooms = self.get_number_of_current_shown_rooms()

    def get_number_of_completed_rooms(self, page_source):
        """:returns the number of completed rooms"""
        return int(BeautifulSoup(page_source, features='html.parser').find('div', {'id': 'rooms-completed'}).text)

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
            if room_name == room or room_name in room:
                return True
        return False
