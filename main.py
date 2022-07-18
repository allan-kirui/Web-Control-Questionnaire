import time

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from passManagement import pwd, username  # used passlib to hash password
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait

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

    time.sleep(0)
    student_button = driver.find_element(By.XPATH, '//a[@href="' + '/auth/app/student' + '"]')

    student_button.click()
    questionnaire_button = None
    time.sleep(5)
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

    # Locating all 2020 modules to click link
    time.sleep(5)

    allEven = driver.find_elements(By.XPATH, '//*[contains(@class,"dtEvenRow")]')
    allEven = len(allEven)
    allOdd = driver.find_elements(By.XPATH, '//*[contains(@class,"dtOddRow")]')
    allOdd = len(allOdd)
    numOfRows = allOdd + allEven

    for row in range(numOfRows):
        firstRow = driver.find_element(By.XPATH, '//*[@id="i1:edt_polls_tbl:tb"]/tr[1]')
        firstRow.click()
        time.sleep(5)
        title = driver.find_element(By.XPATH, '//*[@id="i1"]/div[1]/div/h1/span')
        print(title.text)

        if str(2020) in title.text:
            ankietaNieDotyczy = driver.find_element(By.XPATH, '//*[contains(@value,"dotyczy")]')
            print(ankietaNieDotyczy.text)
            location = ankietaNieDotyczy.location_once_scrolled_into_view
            ankietaNieDotyczy.click()
        else:
            # ticking the checkboxes
            for index in range(9):
                # checkboxes = driver.find_element(By.XPATH, '//*[contains(@id,"'+str(0)+':pnl_qClosedSingle")]')
                # print(checkboxes.text)
                checkboxA = driver.find_element(By.XPATH, '//*[contains(@id,"questions_panel:' + str(index) + '")]//*[contains(@id,"'+str(0)+':pnl_qClosedSingle")]')
                print(checkboxA.text)
                location = checkboxA.location_once_scrolled_into_view
                checkboxA.click()
                time.sleep(5)

            wyslijButton = driver.find_element(By.XPATH, '//*[contains(@value,"odpowiedź")]')
            print(wyslijButton.text)
            location = wyslijButton.location_once_scrolled_into_view
            wyslijButton.click()
            time.sleep(3)
            wyslijConfirm = driver.find_element(By.XPATH,'//*[contains(@id,"i1:j_id")]')
            print(wyslijConfirm.text)
            wyslijConfirm.click()

    # modules = driver.find_elements(By.XPATH, '//span[contains(text(),'+'OCENY'+')]')
    # for module in modules:
    #     print(module.text)
    #     parent_of_module = module.find_element(By.XPATH, '..')
    #     print(parent_of_module.text)
    #     not_involving = parent_of_module.find_element(By.XPATH,  '//span[contains(text(),'+str(2020)+')]' and '//a[@class="' + 'stopEventPropagation' + '"]' )
    #     print(not_involving.text)
    #     not_involving.click()
    #     time.sleep(5)
    #
    #     not_involving_check = parent_of_module.find_element(By.XPATH, '//span[contains(text(),' + str(2020) + ')]').text
    #     print(not_involving_check)
    #     if str(2020) in not_involving_check:
    #         wyslij_button = driver.find_element(By.CLASS_NAME, 'simpleButton')
    #         wyslij_button.click()
    #     else:
    #         anuluj_button = driver.find_element(By.CLASS_NAME, 'leftSpace')
    #         anuluj_button.click()
    #

    # TODO: go through whole list if it contains 2020 accept deletions.
    # TODO: if not, ignore, then another loop to fill in questionnaire

    driver.quit()

except:
    driver.quit()
