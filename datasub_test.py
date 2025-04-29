import pytest, re
from playwright.sync_api import Playwright

main_page_url = 'https://qatest.datasub.com/'

def create_browser(playwright: Playwright):
    return playwright.chromium.launch(headless=False)

def scroll_to(page, locator):    
    page.locator(locator).scroll_into_view_if_needed()

def scroll_and_fill(page, locator, fill):
    scroll_to(page, locator)
    page.locator(locator).fill(fill)

def scroll_and_select_option(page, locator, option):
    scroll_to(page, locator)
    page.select_option(locator, option)

def scroll_and_check(page, locator):
    scroll_to(page, locator)
    page.locator(locator).check()

def scroll_and_click(page, role, target_name):
    target = page.get_by_role(role, name=re.compile(target_name, re.IGNORECASE))
    target.scroll_into_view_if_needed()
    target.click()

def check_is_visible(page, locator, timeout = 5):
    return page.locator(locator).is_visible(timeout=timeout)

@pytest.mark.parametrize('url, title', [('index.html', 'Home'),
                                        ('about.html', 'About'), 
                                        ('quote.html', 'Fee'), 
                                        ('contact.html', 'Contact')])
def test_has_title(playwright: Playwright, url, title):
    browser = create_browser(playwright)
    page = browser.new_page()
    page.goto(main_page_url + url)

    assert f'Startup - {title}' in page.title()
    browser.close()

@pytest.mark.parametrize('purpose', ['Business', 'Personal'])
@pytest.mark.parametrize('withdraws', ['Cash', 'Card' , 'Crypto', 'Cash,Card,Crypto'])
def test_success_form_send(playwright: Playwright, purpose, withdraws):
    browser = create_browser(playwright)
    page = browser.new_page()
    page.goto(main_page_url)

    scroll_to(page, '#subscriptionForm')
    scroll_and_fill(page, '#name', 'test1234')
    scroll_and_fill(page, '#email', 'test1234@mail.ru')
    scroll_and_select_option(page, '#service', 'Select B Service')
    scroll_and_check(page, f"#purpose{purpose}")
    for widthdraw in withdraws.split(','):
        scroll_and_check(page, f"#withdraw{widthdraw}")
    scroll_and_fill(page, '#message', 'Test message 1234567890')
    scroll_and_click(page, 'button', 'request a quote')

    assert(check_is_visible(page, '#formStatus') == True, 'проверка сообщение форма отправлена отображается')
    browser.close()

@pytest.mark.parametrize('email', ['not_email', 'not_full_email@mail'])
def test_not_valid_email_form_send(playwright: Playwright, email):
    browser = create_browser(playwright)
    page = browser.new_page()
    page.goto(main_page_url)

    scroll_to(page, '#subscriptionForm')
    scroll_and_fill(page, '#name', 'test1234')
    scroll_and_fill(page, '#email', email)
    scroll_and_select_option(page, '#service', 'Select B Service')
    scroll_and_check(page, '#purposeBusiness')
    scroll_and_check(page, '#withdrawCash')
    scroll_and_fill(page, '#message', 'Test message 1234567890')
    scroll_and_click(page, 'button', 'request a quote')

    assert(check_is_visible(page, '#formStatus') == False, 'проверка сообщение форма отправлена отображается')
    browser.close()