from dash.testing.application_runners import import_app


# Basic test for the component rendering.
# The dash_duo pytest fixture is installed with dash (v1.0+)
def test_render_component(dash_duo):
    default_state = {
        'chr': '10',
        'start': 114358349,
        'end': 114958349,
        'genome_build': 'GRCh37',
        'variant': "10:114758349_C/T"
    }
    region_size = default_state['start']-default_state['end']
    value=f"{default_state['chr']}:{default_state['start']}-{default_state['end']}"
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
    coordinates.send_keys(new_value)

    # Wait for the text to equal, if after the timeout (default 10 seconds)
    # the text is not equal it will fail the test.
    dash_duo.wait_for_text_to_equal('#region-size', f'Region: {region_size*2:,} bp')