import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import locuszoom_4_dash
import requests, logging, json

from dash import Dash, callback, html, Input, Output, dcc, State, callback_context
from dash.exceptions import PreventUpdate

external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.css',
    'https://cdn.jsdelivr.net/npm/locuszoom@0.14.0/dist/locuszoom.css'
    ]

logger = logging.getLogger()

app = Dash(__name__, external_stylesheets=external_stylesheets)

#Some defaults
BUILD = 'GRCh37'
default_state = {
    'chr': '10',
    'start': 114458349,
    'end': 115058349,
    'genome_build': BUILD,
    'variant': "10:114758349_C/T"
}
max_region_scale = 10_000_000
min_region_scale = 20_000

# Main definition of LocusZoom
LOCAL_API = 'http://127.0.0.1:5000/api'
BASE_API = 'https://portaldev.sph.umich.edu/api/v1'
BASE_API = LOCAL_API
lz = locuszoom_4_dash.Locuszoom4Dash(
        id='lz',
        data_sources=[
            {
                'name': 'gene',
                'data': [
                    'GeneLZ',
                    {
                        'url': f'{BASE_API}/annotation/genes/',
                        'build': BUILD,
                        'trackInfo': f"<strong>ENSEMBL Gene annotation</strong><br>Build: {BUILD}<br></div>",
                    },
                ]
            },
            {
                'name': 'constraint',
                'data': [
                    'GeneConstraintLZ',
                    {
                        'url': 'https://gnomad.broadinstitute.org/api/',
                        'build': BUILD,
                    },
                ]
            },
            {
                'name': 'phewas',
                'data': [
                    'PheWASLZ',
                    {
                        'url': f'{BASE_API}/statistic/phewas/',
                        'build': BUILD,
                        'trackInfo': f"<strong>Phewas source: UMICH</strong><br>Build: {BUILD}<br></div>",
                    },
                ]
            },
        ],
        layout={
            'type':'plot',
            'name':'modified_phewas',
            'override': {
                'max_region_scale': max_region_scale,
                'min_region_scale': min_region_scale,
            },
        },
        state=default_state
    )

app.layout = html.Div([
    lz,
    html.Hr(),
    html.Button(
        'Zoom in (+)',
        id='zoomin',
        n_clicks=0,
    ),
    html.Button(
        'Zoom out (-)',
        id='zoomout',
        n_clicks=0,
    ),
    html.Label('Enter variant to change focus: (Format: CHR:POS_REF/ALT)'),
    html.Div(
        [
            dcc.Input(
                id='variant',
                type='text',
                placeholder='CHR:POS_REF/ALT',
                debounce=True,
                size='39',
            ),
        ],
        style={"width": "15%"},
    ),
    html.P(id='region-size'),
    html.Pre(id='logger'),
])

def parse_variant(variant, state, padding=300_000):
    '''Simple variant parsing'''
    #TODO Check for proper format
    if variant and len(variant) >= 3:
        s = variant.split(':',1)
        g = s[1].split('_',1)
        state['chr'] = s[0]
        state['start'] = max(1,int(g[0]) - padding)
        state['end'] = max(1,int(g[0]) + padding)
        state['variant'] = variant
    return state

@callback(
    Output('lz', 'state'),
    Output('region-size','children'),
    Input('zoomin','n_clicks'),
    Input('zoomout','n_clicks'),
    Input('variant','value'),
    Input('lz','regionChange'),
    State('lz','state'),
    prevent_initial_call=False
)
def change_region(zoomin, zoomout, variant, regionChange, state):
    old_state = state.copy()
    ctx = callback_context
    if len(ctx.triggered) and "zoomin" in ctx.triggered[0]["prop_id"]:
        spread = int(state['end'] - state['start'])
        midpoint = state['start'] + int(spread/2)
        spread = int(min_region_scale/2) if int(spread/2) < min_region_scale else int(spread/4)
        state['start'] =  max(1,midpoint - spread)
        state['end'] =  midpoint + spread
    elif len(ctx.triggered) and "zoomout" in ctx.triggered[0]["prop_id"]:
        spread = int(state['end'] - state['start'])
        midpoint = state['start'] + int(spread/2)
        spread = int(max_region_scale/2) if spread*2 > max_region_scale else spread
        state['start'] =  max(1,midpoint - spread)
        state['end'] =  midpoint + spread
    elif len(ctx.triggered) and "regionChange" in ctx.triggered[0]["prop_id"]:
        state.update(regionChange)
    elif variant:
        state = parse_variant(variant, state)
    return state, f"Region: {state['end']-state['start']:,} bp"

@callback(
    Output('logger','children'),
    Input('lz','elementSelection'),
)
def loggy(element_selection):
    return f'Selected: {json.dumps(element_selection,indent=4)}'

if __name__ == '__main__':
    app.run_server(debug=True)
