# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Locuszoom4Dash(Component):
    """A Locuszoom4Dash component.
Locuszoom4Dash is the DASH version of LocusZoom.js.
It takes ...

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- data_sources (list of dicts; optional):
    Definition of the datasrources for this Locuszoom  Format example:
    [{      name: \"assoc\",      data: [          \"AssociationLZ\",
    {              url:
    \"https://portaldev.sph.umich.edu/api/v1/statistic/single/\",
    source: 45,              id_field: 'variant',
    population: 'ALL',              build: 'GRCh37'          }      ]
    }].

- layout (dict; optional):
    The layout of the Locuszoom plot.  Either choose from one of the 4
    standard layouts, with an optional override, or define the layout
    manually. Example choosing standard layout {      'type': 'plot',
    'name': 'standard_association',      'override': {
    'label_font_size': 20      }  }  'type' should always be plot, may
    be extended in the future 'name' Should be one of
    ['standard_association','association_catalog','standard_phewas','coaccessibility']
    See:
    https://statgen.github.io/locuszoom/docs/api/module-LocusZoom_Layouts.html
    for more on layout options and requirements for the data sources
    Example choosing manual layout {      'width': 800,      'panels':
    [      {          'id' : \"association\",          'height': 300,
    'data_layers': [               {                   'id':
    \"association\",                   'type': \"scatter\",
    'x_axis': { field: \"assoc:position\" },
    'y_axis': { field: \"assoc:log_pvalue\" }               }
    ]      }      ]  }.

- regionChange (dict; optional):
    The change of region, initiated by the user in the LocusZoom plot
    Format example: { state: { chr: 6, start: 20379709, end: 20979709
    } }.

- state (dict; optional):
    The currently selected region for the LocusZoom plot  Format
    example: { state: { chr: 6, start: 20379709, end: 20979709 } }."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'locuszoom_4_dash'
    _type = 'Locuszoom4Dash'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, layout=Component.UNDEFINED, data_sources=Component.UNDEFINED, state=Component.UNDEFINED, regionChange=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'data_sources', 'layout', 'regionChange', 'state']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'data_sources', 'layout', 'regionChange', 'state']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Locuszoom4Dash, self).__init__(**args)
