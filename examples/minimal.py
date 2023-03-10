# To make testing easier during development, adding top directory as module path for easier import
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import locuszoom_4_dash

from dash import Dash, html

external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.css',
    'https://cdn.jsdelivr.net/npm/locuszoom@0.14.0/dist/locuszoom.css'
    ]
data_sources = [
            {
                'name': 'assoc',
                'data': [
                    'AssociationLZ',
                    {
                        'url': 'https://portaldev.sph.umich.edu/api/v1/statistic/single/',
                        'source': 45,
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
]
lz_layout = {
            'type':'plot',
            'name':'standard_association',
}

default_state = {
    'chr': '10',
    'start': 114358349,
    'end': 114958349,
    'genome_build': 'GRCh37',
    'variant': "10:114758349_C/T"
}

app = Dash(__name__, external_stylesheets=external_stylesheets)

# Main definition of LocusZoom
lz = locuszoom_4_dash.Locuszoom4Dash(
        id='lz',
        data_sources=data_sources,
        layout=lz_layout,
        state=default_state
    )

app.layout = html.Div([
    lz,
])

if __name__ == '__main__':
    app.run_server(debug=True)
