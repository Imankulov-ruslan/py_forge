import requests
import pytest
import string
import random

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep


URL = 'https://rioran.github.io/ru_vowels_filter/main.html'

VOWELS = ['а', 'и', 'о', 'у', 'ы', 'э', 'е', 'ё', 'ю', 'я']
CONSONANTS = ['б', 'в', 'г', 'д', 'ж', 'з', 'й', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'ф', 'ч', 'ц', 'ч', 'ш', 'щ']
WHITESPACE = [' ']
PUNCTUATION = string.punctuation


def get_ui_element(xpath, browser):
    return browser.find_element(By.XPATH, xpath)

def clear_input(elem):
    elem.clear()

def set_value(value, elem):
    elem.send_keys(value)

def clear_and_set_value(value, elem):
    clear_input(elem)
    set_value(value, elem)

def get_value(value, elem):
    elem.send_keys(value)

def assert_is_subset(sub_list, super_list):
    assert set(sub_list).issubset(set(super_list)) == True

def create_random_string(*chars, min_length = 1000):
    return ''.join(random.choices(chars, k=min_length))
    
TEXT_WITH_10_VOWELS = create_random_string(*VOWELS, min_length = 10) + create_random_string(*CONSONANTS, *PUNCTUATION, *VOWELS)
TEXT_WITH_10_WHITESPACES = create_random_string(*WHITESPACE, min_length = 10) + create_random_string(*CONSONANTS, *PUNCTUATION, *VOWELS)
TEXT_WITH_10_PUNCTUATION = create_random_string(*PUNCTUATION, min_length = 10) + create_random_string(*CONSONANTS, *PUNCTUATION, *VOWELS)

@pytest.mark.parametrize(
        'input_string', 
        ['default', TEXT_WITH_10_VOWELS, '']
    )
def test_ru_vowels_filter(browser, input_string):
    browser.get(URL)

    vowels_btn = get_ui_element("/html/body/div/div[2]/button[1]", browser)
    input_textarea = get_ui_element("/html/body/div/div[1]/textarea", browser)
    output_textarea = get_ui_element("/html/body/div/div[3]/div", browser)

    if input_string == 'default':
        vowels_btn.click()
        assert len(output_textarea.text) !=0
        for elem in output_textarea.text.split('\n'):
            assert_is_subset(elem, VOWELS)

    elif input_string == TEXT_WITH_10_VOWELS:
        clear_and_set_value(input_string,input_textarea)
        vowels_btn.click()
        assert len(output_textarea.text) >= 10
        for elem in output_textarea.text.split('\n'):
            assert_is_subset(elem, VOWELS)

    else:
        clear_and_set_value(input_string,input_textarea)
        vowels_btn.click()
        assert len(output_textarea.text) == 0


@pytest.mark.parametrize(
        'input_string', 
        ['default', TEXT_WITH_10_WHITESPACES, '']
    )
def test_ru_vowels_spaces_filter(browser, input_string):
    browser.get(URL)

    spaces_button = get_ui_element("/html/body/div/div[2]/button[2]", browser)
    input_textarea = get_ui_element("/html/body/div/div[1]/textarea", browser)
    output_textarea = get_ui_element("/html/body/div/div[3]/div", browser)

    if input_string == 'default':
        spaces_button.click()
        assert len(output_textarea.text) !=0
        for elem in output_textarea.text.split('\n'):
            assert_is_subset(elem, [*VOWELS, *WHITESPACE])

    elif input_string == TEXT_WITH_10_WHITESPACES:
        clear_and_set_value(input_string, input_textarea)
        spaces_button.click()
        assert len(output_textarea.text) >= 10
        for elem in output_textarea.text.split('\n'):
            assert_is_subset(elem, [*VOWELS, *WHITESPACE])

    else:
        clear_and_set_value(input_string, input_textarea)
        spaces_button.click()
        assert len(output_textarea.text) == 0


@pytest.mark.parametrize(
        'input_string', 
        ['default', TEXT_WITH_10_PUNCTUATION, '']
    )
def test_ru_vowels_punctuation_filter(browser, input_string):
    browser.get(URL)

    punctuation_button = get_ui_element("/html/body/div/div[2]/button[3]", browser)
    input_textarea = get_ui_element("/html/body/div/div[1]/textarea", browser)
    output_textarea = get_ui_element("/html/body/div/div[3]/div", browser)

    if input_string == 'default':
        punctuation_button.click()
        assert len(output_textarea.text) !=0
        for elem in output_textarea.text.split('\n'):
            assert_is_subset(elem, [*VOWELS, *PUNCTUATION, *WHITESPACE])

    elif input_string == TEXT_WITH_10_PUNCTUATION:
        clear_and_set_value(input_string,input_textarea)
        punctuation_button.click()
        assert len(output_textarea.text) >= 10
        for elem in output_textarea.text.split('\n'):
            assert_is_subset(elem, [*VOWELS, *PUNCTUATION, *WHITESPACE])

    else:
        clear_and_set_value(input_string,input_textarea)
        punctuation_button.click()
        assert len(output_textarea.text) == 0

def test_select_button(browser):
    browser.get(URL)

    select_button = get_ui_element("/html/body/div/div[2]/button[4]", browser)
    output_text = get_ui_element("/html/body/div/div[3]/div", browser).text

    select_button.click()
    selected_text = browser.execute_script("return window.getSelection().toString();")

    assert output_text == selected_text

def test_button_positions(browser):
    browser.get(URL)
    browser.maximize_window()

    vowels_btn = get_ui_element("/html/body/div/div[2]/button[1]", browser)
    spaces_button = get_ui_element("/html/body/div/div[2]/button[2]", browser)
    punctuation_button = get_ui_element("/html/body/div/div[2]/button[3]", browser)
    select_button = get_ui_element("/html/body/div/div[2]/button[4]", browser)

    assert vowels_btn.location['y'] == spaces_button.location['y'] == punctuation_button.location['y'] == select_button.location['y']

    browser.set_window_size(400, 600)
    assert select_button.location['x'] == vowels_btn.location['x']
    assert select_button.location['y'] > vowels_btn.location['y']
