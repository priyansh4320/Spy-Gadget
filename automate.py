import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Choose the appropriate WebDriver for your browser (e.g., Chrome, Firefox)
def pimeye():
    driver = webdriver.Chrome()  # Change to webdriver.Firefox() for Firefox

    # Open the website
    driver.get("https://pimeyes.com/en/login")  # Replace with the URL of the website you want to login to

    # Find the login form elements (e.g., username and password fields, su
    #login
    type_attribute_value_pass = "password" 
    type_attribute_value_user = "email" 
    username = driver.find_element(By.XPATH, f'//*[@type="{type_attribute_value_user}"]')  # Replace "username" with the actual ID of the username field
    password = driver.find_element(By.XPATH, f'//*[@type="{type_attribute_value_pass}"]')  # Replace "password" with the actual ID of the password field
    submit_button = driver.find_element(By.CLASS_NAME, "login-btn")  # Replace "login-button" with the actual ID of the submit button

    # Enter your login credentials
    username.send_keys("aimagic123@mailinator.com")
    password.send_keys("Aiismagic123!")
    driver.find_element(By.XPATH,f'//input[@name="remember"]').click()
    submit_button.click()
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"icon notranslate")))
    #open homepage
    home_attribute = "Open mainpage"

    homepage = driver.find_element(By.XPATH, f'//*[@aria-label="{home_attribute}"]')
    link_url = homepage.get_attribute("href")
    driver.execute_script(f'window.open("{link_url}");')
    driver.switch_to.window(driver.window_handles[-1])


    #upload faces
    driver.find_element(By.CLASS_NAME,"understand").click()
    driver.find_element(By.CLASS_NAME,"upload").click()
    #time.sleep(30)
    '''
    search = '//button[@data-v-4551e51b=""]'
    search = WebDriverWait(driver, 20).until(
        EC.visibility_of_any_elements_located((By.XPATH, search))
    )
    search[0].click()
    search[-1].click()
    '''
    #start reverse search
    checkbox = "checkbox"
    checkbox = WebDriverWait(driver, 60).until(
        EC.visibility_of_any_elements_located((By.XPATH, f'//*[@type="{checkbox}"]'))
    )
    for i in checkbox:
        i.click()

    buttons = driver.find_elements(By.XPATH,f'//button[@data-v-a60bceaf=""]')
    buttons[3].click()


    #export result csv
    start_time = time.time()
    while(True):
        export = 'download'
        export = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, f'//*[@alt="{export}"]'))
        )
        export.click()

        filename = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "filename"))
        )
        filename.send_keys("results")

        export_csv = driver.find_element(By.XPATH,f'//button[@data-v-bbba1abc=""]').click()

        if WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.CLASS_NAME,"container limited-container"))).click():
            driver.close()
        upload_agian = WebDriverWait(driver, 120).until(
            EC.visibility_of_element_located((By.XPATH, f'//button[@data-v-7e26e312=""]'))
        )
        upload_agian.click()

        search_agian = WebDriverWait(driver, 30).until(
            EC.visibility_of_any_elements_located((By.XPATH, f'//button[@data-v-a60bceaf=""]'))
        )
        search_agian[3].click()
        

        pass

#driver.execute_script("arguments[0].click();", button)


time.sleep(300)
#driver2 = webdriver.Chrome()
#driver2.get("https://www.mailinator.com/v4/public/inboxes.jsp?to=aimagic123")

#driver2.find_element(By.CLASS_NAME,"ng-binding").click()
#driver2.find_element(By.CLASS_NAME,"button button-primary").click()
# Wait for a specific condition (e.g., the presence of an element on the redirected page)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "welcome-message")))

#driver2.quit()
