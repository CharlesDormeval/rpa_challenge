import pandas as pd
from time import sleep
from typing import Union
from logging import error
from selenium import webdriver
from traceback import format_exc
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import InvalidSessionIdException

from constants import CHALLENGE_URL, N_ROUNDS, ELEMENTS_FORM
from input_interactions import start_challenge, find_inputs_by_label, fill_inputs, next_round


def complete_rpa_challenge(input_data:pd.DataFrame):
    """
    Complete RPA challenge round after round

    :param input_data: excel content (pd.read_excel/pd.read_csv)
    :type input_data: pd.DataFrame
    """
    challenge_session = create_challenge_session()
    if not challenge_session:
        return
    start_challenge(challenge_session)
    for current_round in range(N_ROUNDS):
        round_data = get_data_for_round(current_round, input_data)
        fill_challenge_form(round_data, challenge_session)
    sleep(2)
    close_challenge_session(challenge_session)


def fill_challenge_form(round_data:pd.Series, session:WebDriver):
    """
    Fill form with given data

    :param round_data: data to use for current round
    :type round_data: pd.Series
    :param session: session webdriver
    :type session: WebDriver
    """
    web_elements = find_inputs_by_label(ELEMENTS_FORM, session)
    fill_inputs(web_elements, round_data)
    next_round(session)


def create_challenge_session() -> Union[WebDriver, None]:
    """
    Create a chromium webdriver and access challenge url with it.

    :return: None if a problem occure during the creation of the driver (+ access to the challenge page), else webdriver
    :rtype: Union[WebDriver, None]
    """
    driver = None
    try:
        driver = webdriver.Chrome()
        driver.get(CHALLENGE_URL)
    except InvalidSessionIdException as e:
        error(e)
        if driver:
            close_challenge_session(driver)
        driver = None
    except:
        error("Something went wrong while creating driver or accessing challenge page:")
        error(format_exc())
        if driver:
            close_challenge_session(driver)
        driver = None
    return driver


def close_challenge_session(challenge_session:WebDriver):
    """
    Close session webdriver

    :param challenge_session: driver to close
    :type challenge_session: WebDriver
    """
    challenge_session.close()


def get_data_for_round(round:int, input_data:pd.DataFrame) -> Union[pd.Series, None]:
    """
    Get data to use in each round

    :param round: current round
    :type round: int
    :param input_data: data to use for RPA challenge
    :type input_data: pd.DataFrame
    :return: data Series to use for current round, None if round data could not be accessed
    :rtype: Union[pd.Series, None]
    """
    try:
        return input_data.iloc[round]
    except IndexError:
        print('Error getting data for round')
        return None
    