import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import subprocess
import os
import signal

FLASK_PROC = None

@pytest.fixture(scope="session", autouse=True)
def start_server():
    global FLASK_PROC

    project_root = os.path.join(os.path.dirname(__file__), "..")

    FLASK_PROC = subprocess.Popen(
        ["python", "-m", "backend.app"],
        cwd=project_root
    )

    time.sleep(2)  # darle tiempo a que arranque

    yield

    FLASK_PROC.terminate()
    try:
        FLASK_PROC.wait(timeout=5)
    except:
        FLASK_PROC.kill()

@pytest.fixture(autouse=True)
def clean_db():
    from backend.repository import reset_all
    reset_all()
    yield


@pytest.fixture(scope="session")
def browser():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()



