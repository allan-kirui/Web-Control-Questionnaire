import time

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


def locateAndConfirmSend(driver):
    # Locating and clicking the confirm button
    wyslijConfirm = driver.find_element(By.XPATH, '//*[contains(@id,"i1:j_id")][contains(@value,"odpowiedź")]')
    print(wyslijConfirm.text, wyslijConfirm.accessible_name, wyslijConfirm.location)
    locationWyslijConfirm = wyslijConfirm.location_once_scrolled_into_view
    driver.execute_script("arguments[0].click();", WebDriverWait(driver, AJAX_WAIT_TIME).until(
        EC.element_to_be_clickable((By.XPATH, '//*[contains(@id,"i1:j_id")][contains(@value,"odpowiedź")]'))))
    time.sleep(FAST_WAIT_TIME)


driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))

# Our enauczanie log in page
driver.get(
    'https://moja.pg.edu.pl/')

try:

    # Find login button
    first_login_button = driver.find_element(By.CLASS_NAME, "btn-primary")

    # Click login
    first_login_button.click()

    # Select the id box
    id_box = driver.find_element(By.ID, 'username')

    # Send id information
    id_box.send_keys(username)

    # Find password box
    pass_box = driver.find_element(By.ID, 'password')

    # Send password
    pass_box.send_keys(pwd)

    # Find login button
    login_button = driver.find_element(By.ID, 'submit_button')

    # Click login
    login_button.click()

    # Find Proceed Button after login
    proceed_button = driver.find_element(By.CLASS_NAME, 'btn-submit')

    # Click proceed_button
    proceed_button.click()

    student_button = driver.find_element(By.XPATH, '//a[@href="' + '/auth/app/student' + '"]')

    student_button.click()
    questionnaire_button = None
    time.sleep(NORMAL_WAIT_TIME)
    toggle = driver.find_element(By.XPATH, '//a[@rel="' + 'menu-start' + '"]')

    try:
        toggle.click()
    except:
        menu_toggle = driver.find_element(By.ID, "menu-tabs-toggle")
        menu_toggle.click()
        toggle = driver.find_element(By.XPATH, '//a[@rel="' + 'menu-start' + '"]')
        toggle.click()
    finally:
        questionnaire_button = driver.find_element(By.ID, "j_id191")
        questionnaire_button.click()

    time.sleep(NORMAL_WAIT_TIME)

    # Calculates the number of questionnaires
    allEven = driver.find_elements(By.XPATH, '//*[contains(@class,"dtEvenRow")]')
    allEven = len(allEven)
    allOdd = driver.find_elements(By.XPATH, '//*[contains(@class,"dtOddRow")]')
    allOdd = len(allOdd)
    numOfRows = allOdd + allEven

    # Goes through each row, and performs appropriate actions for each row
    for row in range(numOfRows):
        # Selects first row
        firstRow = driver.find_element(By.XPATH, '//*[@id="i1:edt_polls_tbl:tb"]/tr[1]')
        locationFirstRow = firstRow.location_once_scrolled_into_view
        firstRow.click()
        time.sleep(NORMAL_WAIT_TIME)

        # Gets the title of the questionnaire
        title = driver.find_element(By.XPATH, '//*[@id="i1"]/div[1]/div/h1/span')
        print(title.text)

        if "MODUŁU 2020" in title.text:  # Indicates that this is an old questionnaire a.k.a not meant to be filled by us
            ankietaNieDotyczy = driver.find_element(By.XPATH, '//*[contains(@value,"dotyczy")]')
            print(ankietaNieDotyczy.text, ankietaNieDotyczy.accessible_name, ankietaNieDotyczy.location)
            location = ankietaNieDotyczy.location_once_scrolled_into_view  # Scrolls to the element
            ankietaNieDotyczy.click()

            # Locates the confirm send button
            locateAndConfirmSend(driver)
        else:
            # Ticking the checkboxes
            for index in range(NUM_OF_CHECKBOXES):
                # Locates the checkbox
                checkboxA = driver.find_element(By.XPATH, '//*[contains(@id,"questions_panel:' + str(
                    index) + '")]//*[contains(@id,"' + str(0) + ':pnl_qClosedSingle")]')
                print(checkboxA.text)
                locationCheckboxA = checkboxA.location_once_scrolled_into_view
                checkboxA.click()
                time.sleep(FAST_WAIT_TIME)

            # Sends our filled questionnaire
            wyslijButton = driver.find_element(By.XPATH, '//*[contains(@value,"odpowiedź")]')
            print(wyslijButton.text, wyslijButton.location)
            locationWyslijButton = wyslijButton.location_once_scrolled_into_view
            wyslijButton.click()
            time.sleep(NORMAL_WAIT_TIME)

            # Locating and clicking the confirm button
            locateAndConfirmSend(driver)

    driver.quit()

except Exception as e:
    print(e)
    driver.quit()
