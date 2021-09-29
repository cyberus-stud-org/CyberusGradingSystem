from bs4 import BeautifulSoup
from time import sleep

import config


class THMProfile:

    def __init__(self, driver, username):

        self.driver = driver
        self.driver.get(config.THM_PROFILE_URL + username)

        try:
            number_of_completed_rooms = self.get_number_of_completed_rooms(self.driver.page_source)
        except:
            sleep(3)
            number_of_completed_rooms = self.get_number_of_completed_rooms(self.driver.page_source)

        number_of_current_shown_rooms = self.get_number_of_current_shown_rooms()

        while number_of_current_shown_rooms < number_of_completed_rooms:
            self.show_more_rooms()
            number_of_current_shown_rooms = self.get_number_of_current_shown_rooms()

    def get_number_of_completed_rooms(self, page_source):
        return int(BeautifulSoup(page_source, features='html.parser').find('div', {'id': 'rooms-completed'}).text)

    def get_number_of_current_shown_rooms(self):
        soup = BeautifulSoup(self.driver.page_source, features='html.parser')
        return len(soup.find_all('div', {'class': 'room-card-design-title'}))

    def show_more_rooms(self):
        self.driver.execute_script('completedRoomsAdd()')

    def get_all_completed_rooms(self):
        soup = BeautifulSoup(self.driver.page_source, features='html.parser')
        return [room_name.text for room_name in soup.find_all('div', {'class': 'room-card-design-title'})]
