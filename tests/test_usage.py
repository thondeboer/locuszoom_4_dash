from dash.testing.application_runners import import_app
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

default_state = {
    'chr': '10',
    'start': 114358349,
    'end': 114958349,
    'genome_build': 'GRCh37',
    'variant': "10:114758349_C/T"
}
region_size = default_state['end']-default_state['start']
value=f"{default_state['chr']}:{default_state['start']}-{default_state['end']}"

# Basic test for the component rendering.
# The dash_duo pytest fixture is installed with dash (v1.0+)
def test_render_component(dash_duo):
    # Start a dash app contained as the variable `app` in `usage.py`
    app = import_app('usage')
    dash_duo.start_server(app)

    # Get the generated component input with selenium
    coordinates = dash_duo.find_element('#coordinates')
    assert value == coordinates.get_attribute('value')
    dash_duo.wait_for_text_to_equal('#region-size', f'Region: {region_size:,} bp')

# 17:40896312-41577500
def test_enter_coordinates(dash_duo):
    new_value = f"{default_state['chr']}:{default_state['start']-int(region_size/2)}-{default_state['end']+int(region_size/2)}"
    # Start a dash app contained as the variable `app` in `usage.py`
    app = import_app('usage')
    dash_duo.start_server(app)

    # Get the generated component input with selenium
    coordinates = dash_duo.find_element('#coordinates')
    assert value == coordinates.get_attribute('value')
    dash_duo.wait_for_text_to_equal('#region-size', f'Region: {region_size:,} bp')

    # Clear the input
    dash_duo.clear_input(coordinates)

    # Send a new region to focus on that is twice the size.
    coordinates.send_keys(new_value, Keys.RETURN)

    # Wait for the text to equal, if after the timeout (default 10 seconds)
    # the text is not equal it will fail the test.
    dash_duo.wait_for_text_to_equal('#region-size', f'Region: {region_size*2:,} bp')

def test_enter_gene(dash_duo):
    # Start a dash app contained as the variable `app` in `usage.py`
    app = import_app('usage')
    dash_duo.start_server(app)

    # Get the generated component input with selenium
    coordinates = dash_duo.find_element('#gene')

    # Send the gene to focus
    coordinates.send_keys('brca1', Keys.RETURN)
    dash_duo.wait_for_text_to_equal('#coordinates', '17:40896312-41577500')
    dash_duo.wait_for_text_to_equal('#region-size', 'Region: 681,188 bp')

def test_zoomin(dash_duo):
    zoomed_in_region = f"{default_state['chr']}:{default_state['start']+int(region_size/4)}-{default_state['end']-int(region_size/4)}"
    zoomed_in_value = int(region_size/2)
    # Start a dash app contained as the variable `app` in `usage.py`
    app = import_app('usage')
    dash_duo.start_server(app)

    # Get the button
    zoom_in = dash_duo.find_element('#zoomin')

    # Zoom in
    zoom_in.click()
    dash_duo.wait_for_text_to_equal('#coordinates', zoomed_in_region)
    dash_duo.wait_for_text_to_equal('#region-size', f'Region: {zoomed_in_value:,} bp')
    dash_duo.driver.refresh()

def test_zoomout(dash_duo):
    zoomed_out_region = f"{default_state['chr']}:{default_state['start']-int(region_size/2)}-{default_state['end']+int(region_size/2)}"
    zoomed_out_value = region_size*2
    # Start a dash app contained as the variable `app` in `usage.py`
    app = import_app('usage')
    dash_duo.start_server(app)

    # Get the button
    zoom_out = dash_duo.find_element('#zoomout')

    # Zoom out
    zoom_out.click()
    dash_duo.wait_for_text_to_equal('#coordinates', zoomed_out_region)
    dash_duo.wait_for_text_to_equal('#region-size', f'Region: {zoomed_out_value:,} bp')