from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from mod_utilize import app

def test_homepage_ui(live_server):
    driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed
    driver.get(live_server.url)
    
    assert "Breathe In" in driver.title
    
    start_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "start-meditation"))
    )
    assert start_button.is_displayed()
    
    driver.quit()

# Add more UI tests for different pages and interactions

def test_invalid_meditation_id(client):
    response = client.get('/meditation/9999')  # Assuming 9999 is an invalid ID
    assert response.status_code == 404

def test_empty_feedback_submission(client, login_user):
    response = client.post('/submit_feedback', data={'feedback': ''})
    assert response.status_code == 400  # Expecting a bad request response