import locuszoom_4_dash
import requests, logging

from dash import Dash, callback, html, Input, Output, dcc, State, callback_context
from dash.exceptions import PreventUpdate
from flask import Flask

external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.css',
    'https://cdn.jsdelivr.net/npm/locuszoom@0.14.0/dist/locuszoom.css'
    ]

logger = logging.getLogger()

server = Flask(__name__)

app = Dash(
    server=server,
    external_stylesheets = external_stylesheets,
)

#Some defaults
default_state = {
    'chr': '10',
    'start': 114358349,
    'end': 114958349,
    'genome_build': 'GRCh37',
    'variant': "10:114758349_C/T"
}
max_region_scale = 10_000_000
min_region_scale = 20_000

# Main definition of LocusZoom
# This contains many of the data sources from the Samples, but not all plots use all data sources
lz = locuszoom_4_dash.Locuszoom4Dash(
        id='lz',
        data_sources=[
            {
                'name': 'assoc',
                'data': [
                    'AssociationLZ',
                    {
                        'url': 'http://10.112.80.49:16888/api/statistic/single/',
                        'source': 'AD',
                        'id_field':'variant',
                        'build': 'GRCh37',
                    },
                ]
            },
            {
                'name': 'ld',
                'data': [
                    'LDServer',
                    {
                        'url': 'https://portaldev.sph.umich.edu/ld/',
                        'source': '1000G',
                        'population': 'ALL',
                        'build': 'GRCh37',
                    },
                ]
            },
            {
                'name': 'recomb',
                'data': [
                    'RecombLZ',
                    {
                        'url': 'https://portaldev.sph.umich.edu/api/v1/annotation/recomb/results/',
                        'build': 'GRCh37',
                    },
                ]
            },
            {
                'name': 'gene',
                'data': [
                    'GeneLZ',
                    {
                        'url': 'https://portaldev.sph.umich.edu/api/v1/annotation/genes/',
                        'build': 'GRCh37',
                    },
                ]
            },
            {
                'name': 'constraint',
                'data': [
                    'GeneConstraintLZ',
                    {
                        'url': 'https://gnomad.broadinstitute.org/api/',
                        'build': 'GRCh37',
                    },
                ]
            },
            {
                'name': 'catalog',
                'data': [
                    'GwasCatalogLZ',
                    {
                        'url': 'https://portaldev.sph.umich.edu/api/v1/annotation/gwascatalog/results/',
                        'build': 'GRCh37',
                    },
                ]
            },
            {
                'name': 'phewas',
                'data': [
                    'PheWASLZ',
                    {
                        'url': 'http://10.112.80.49:16888/api/statistic/phewas/',
                        'build': 'GRCh37',
                    },
                ]
            },
        ],
        layout={
            'type':'plot',
            'name':'association_catalog',
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
    html.Label('Enter Gene symbol to change focus:'),
    html.Div(
        [
            dcc.Input(
                id='gene',
                type='text',
                placeholder='Gene symbol',
                debounce=True,
                size='39',
            ),
            html.Label('OR enter coordinates (GRCh37/hg19):'),
            dcc.Input(
                id='coordinates',
                type='text',
                value=f"{default_state['chr']}:{default_state['start']}-{default_state['end']}",
                placeholder='e.g. 10:123-456 or X:789',
                debounce=True,
                size='39',
            ),
        ],
        style={"width": "15%"},
    ),
    html.P(id='region-size'),
])

def get_gene_location(gene, padding=300_000):
    '''Use myGene.info API to find the location of the gene symbol'''
    base_url = 'https://mygene.info/v3/query'
    query = {
        'q':f'symbol:{gene}',
        'fields': 'genomic_pos_hg19',
        'species':'human',
        'ensemblonly': True
    }
    r = requests.get(base_url, params=query)
    j = r.json()
    hits = j.get('hits')
    if len(hits) > 0:
        #Just take the first
        return {
            'chr': hits[0]['genomic_pos_hg19']['chr'],
            'start': hits[0]['genomic_pos_hg19']['start']-padding,
            'end': hits[0]['genomic_pos_hg19']['end']+padding,
        }

def parse_coordinates(coordinates, padding=300_000):
    '''Simple coordinate parsing. Padding added when single position is provided'''
    res = {}
    if coordinates and len(coordinates) >= 3:
        s = coordinates.split(':',1)
        g = s[1].split('-',1)
        res['chr'] = s[0]
        res['start'] = max(1,int(g[0]) - padding) if len(g) == 1 else max(1,int(g[0]))
        res['end'] = max(1,int(g[0]) + padding) if len(g) == 1 else max(1,int(g[1]))
    return res

@callback(
    Output('lz', 'state'),
    Output('gene','value'),
    Output('coordinates','value'),
    Output('region-size','children'),
    Input('zoomin','n_clicks'),
    Input('zoomout','n_clicks'),
    Input('gene','value'),
    Input('lz','regionChange'),
    Input('coordinates','value'),
    State('lz','state'),
    prevent_initial_call=False
)
def change_region(zoomin, zoomout, gene, regionChange, coordinates, state):
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
    elif gene:
        state = get_gene_location(gene)
    elif coordinates:
        state = parse_coordinates(coordinates)
    if old_state == state:
        raise PreventUpdate
    #Clear out gene value so user could enter coordinates later
    return state, '', f"{state['chr']}:{state['start']}-{state['end']}", f"Region: {state['end']-state['start']:,} bp"

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
