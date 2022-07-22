import time
import re

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from passManagement import pwd, username  # used passlib to hash password
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

NORMAL_WAIT_TIME = 5  # Seconds to wait
FAST_WAIT_TIME = 2
AJAX_WAIT_TIME = 20
NUM_OF_CHECKBOXES = 9


class Questionnaire:
    username = None
    password = None
    filepath = None
    driver = None
    professorDetails = None
    numOfQuestionnaireRows = None
    professorName = None
    professorRole = None
    matchingProfessor = None

    def __init__(self, username, password, filepath):
        self.userDetails(username, password, filepath)
        self.processFile()
        self.setupDriver()
        self.main()

    def userDetails(self, username, password, filepath):
        self.username = username
        self.password = password
        self.filepath = filepath

    def processFile(self):
        # getting professor names
        with open(self.filepath, encoding='utf-8') as file:
            next(file)
            professors = [line.rstrip() for line in file]

        self.professorDetails = [professor_detail.split(' - ') for professor_detail in professors]
        self.professorDetails = self.replacer()

    def setupDriver(self):
        self.driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))

        # Our enauczanie log in page
        self.driver.get(
            'https://moja.pg.edu.pl/')

    def login(self):
        # Find login button
        first_login_button = self.driver.find_element(By.CLASS_NAME, "btn-primary")

        # Click login
        first_login_button.click()

        # Select the id box
        id_box = self.driver.find_element(By.ID, 'username')

        # Send id information
        id_box.send_keys(username)

        # Find password box
        pass_box = self.driver.find_element(By.ID, 'password')

        # Send password
        pass_box.send_keys(pwd)

        # Find login button
        login_button = self.driver.find_element(By.ID, 'submit_button')

        # Click login
        login_button.click()

        # Find Proceed Button after login
        proceed_button = self.driver.find_element(By.CLASS_NAME, 'btn-submit')

        # Click proceed_button
        proceed_button.click()

    def locateQuestionnaires(self):
        student_button = self.driver.find_element(By.XPATH, '//a[@href="' + '/auth/app/student' + '"]')

        student_button.click()
        questionnaire_button = None
        time.sleep(NORMAL_WAIT_TIME)
        toggle = self.driver.find_element(By.XPATH, '//a[@rel="' + 'menu-start' + '"]')

        try:
            toggle.click()
        except Exception as e:  # in case of switched dimensions of screen therefore, toggle located in different
            # location
            print(e)
            menu_toggle = self.driver.find_element(By.ID, "menu-tabs-toggle")
            menu_toggle.click()
            toggle = self.driver.find_element(By.XPATH, '//a[@rel="' + 'menu-start' + '"]')
            toggle.click()
        finally:
            questionnaire_button = self.driver.find_element(By.ID, "j_id191")
            questionnaire_button.click()

        time.sleep(NORMAL_WAIT_TIME)

    def calculateNumberOfQuestionnaires(self):
        # Calculates the number of questionnaires
        allEven = self.driver.find_elements(By.XPATH, '//*[contains(@class,"dtEvenRow")]')
        allEven = len(allEven)
        allOdd = self.driver.find_elements(By.XPATH, '//*[contains(@class,"dtOddRow")]')
        allOdd = len(allOdd)
        self.numOfQuestionnaireRows = allOdd + allEven

    def findMatchingProfessor(self):
        self.professorName = self.driver.find_element(By.XPATH,
                                                      '//*[contains(@id,"i1:j_id")]/table/tbody/tr[2]/td[2]')
        self.professorRole = self.driver.find_element(By.XPATH,
                                                      '//*[contains(@id,"i1:j_id")]/table/tbody/tr[4]/td[2]/span')
        print(self.professorName.text, self.professorName.accessible_name, self.professorName.location)
        print(self.professorRole.text, self.professorRole.accessible_name, self.professorRole.location)

        # prof_det[0] contains professor_name, checks if one of the names in our list matches the one in
        # website
        # prof_det[1] contains professor_role, checks if one of the roles in our list matches the
        # one in website
        self.matchingProfessor = [prof_detail for prof_detail in self.professorDetails if
                                  prof_detail[0] in self.professorName.text and self.professorRole.text in
                                  prof_detail[
                                      1]]

    # Locating and clicking the confirm button on the website
    def locateAndConfirmSend(self):
        wyslijConfirm = self.driver.find_element(By.XPATH, '//*[contains(@id,"i1:j_id")][contains(@value,"odpowiedź")]')
        print(wyslijConfirm.text, wyslijConfirm.accessible_name, wyslijConfirm.location)
        locationWyslijConfirm = wyslijConfirm.location_once_scrolled_into_view
        self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, AJAX_WAIT_TIME).until(
            EC.element_to_be_clickable((By.XPATH, '//*[contains(@id,"i1:j_id")][contains(@value,"odpowiedź")]'))))
        time.sleep(FAST_WAIT_TIME)

    # Situation where software is supposed to skip filling in a questionnaire
    def questionnaireNotForUser(self):
        ankietaNieDotyczy = self.driver.find_element(By.XPATH, '//*[contains(@value,"dotyczy")]')
        print(ankietaNieDotyczy.text, ankietaNieDotyczy.accessible_name, ankietaNieDotyczy.location)
        location = ankietaNieDotyczy.location_once_scrolled_into_view  # Scrolls to the element
        ankietaNieDotyczy.click()

        # Locates the confirm send button
        self.locateAndConfirmSend()

    # replaces the shortforms in professorList with appropriate values
    def replacer(self):
        for detail in self.professorDetails:
            detail[1] = re.sub("P", "Projekt", detail[1])
            detail[1] = re.sub("W", "Wykład", detail[1])
            detail[1] = re.sub("C", "Ćwiczenia", detail[1])
            detail[1] = re.sub("L", "Laboratorium", detail[1])
        return self.professorDetails

    def main(self):

        try:

            self.login()

            self.locateQuestionnaires()

            self.calculateNumberOfQuestionnaires()

            # Goes through each row, and performs appropriate actions for each row
            for row in range(self.numOfQuestionnaireRows):
                # Selects first row
                firstRow = self.driver.find_element(By.XPATH, '//*[@id="i1:edt_polls_tbl:tb"]/tr[1]')
                locationFirstRow = firstRow.location_once_scrolled_into_view
                firstRow.click()
                time.sleep(NORMAL_WAIT_TIME)

                # Gets the title of the questionnaire
                title = self.driver.find_element(By.XPATH, '//*[@id="i1"]/div[1]/div/h1/span')
                print(title.text)

                if "MODUŁU 2020" in title.text:  # Indicates that this is an old questionnaire a.k.a. not meant to be
                    # filled by us
                    self.questionnaireNotForUser()
                else:
                    self.findMatchingProfessor()

                    if len(self.matchingProfessor) == 0:
                        self.questionnaireNotForUser()
                    else:
                        # Ticking the checkboxes
                        for index in range(NUM_OF_CHECKBOXES):
                            # Locates the checkbox
                            checkboxA = self.driver.find_element(By.XPATH, '//*[contains(@id,"questions_panel:' + str(
                                index) + '")]//*[contains(@id,"' + str(0) + ':pnl_qClosedSingle")]')
                            print(checkboxA.text)
                            locationCheckboxA = checkboxA.location_once_scrolled_into_view
                            checkboxA.click()
                            time.sleep(FAST_WAIT_TIME)

                        # Sends our filled questionnaire
                        sendButton = self.driver.find_element(By.XPATH, '//*[contains(@value,"odpowiedź")]')
                        print(sendButton.text, sendButton.location)
                        locationWyslijButton = sendButton.location_once_scrolled_into_view
                        sendButton.click()
                        time.sleep(NORMAL_WAIT_TIME)

                        # Locating and clicking the confirm button
                        self.locateAndConfirmSend()

            self.driver.quit()

        except Exception as e:
            print(e)
            self.driver.quit()



