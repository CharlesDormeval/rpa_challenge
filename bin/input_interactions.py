import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


def start_challenge(session:WebDriver) -> None:
    """
    Start challenge by clicking on start button

    :param session: session webdriver
    :type session: WebDriver
    """
    button = session.find_element(By.XPATH, '//button[text()="Start"]')
    button.click()


def next_round(session:WebDriver) -> None:
    """
    Start next round by clicking on submit button

    :param session: session webdriver
    :type session: WebDriver
    """
    all_inputs = session.find_elements(By.TAG_NAME, 'input')
    for input in all_inputs:
        if input.get_attribute('value') == 'Submit':
            input.click()
            return


def find_inputs_by_label(name_of_elements:list, session:WebDriver) -> dict:
    """
    Find input elements corresponding to list content

    :param name_of_elements: text of elements to find on page
    :type name_of_elements: list
    :param session: session webdriver
    :type session: WebDriver
    :return: values for inputs
    :rtype: dict
    """
    inputs = dict()
    for name in name_of_elements:
        input = session.find_element(By.XPATH, f'//label[text()="{name}"]/following-sibling::input')
        # Associate input to its column (ex: inputs['First Name'] = name input in challenge page)
        inputs[name] = input
    return inputs


def fill_inputs(inputs:dict, data:pd.Series):
    """
    Fill inputs with given data

    :param inputs: inputs from find_inputs_by_label
    :type inputs: dict
    :param data: data corresponding to inputs
    :type data: pd.Series
    """
    for key in inputs.keys():
        data_for_key = data[key]
        inputs[key].send_keys(data_for_key)
