from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from passManagement import pwd, username  # used passlib to hash password



driver = webdriver.Edge(EdgeChromiumDriverManager().install())

# Our enauczanie log in page
driver.get(
    'https://logowanie.pg.edu.pl/login?service=https%3A%2F%2Fenauczanie.pg.edu.pl%2Fmoodle%2Flogin%2Findex.php%3FauthCAS%3DCAS')
try:
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
    proceed_button = driver.find_element(By.CLASS_NAME,'btn-submit')

    # Click proceed_button
    proceed_button.click()

    driver.quit()

except:
    driver.quit()