# AUTO GENERATED FILE - DO NOT EDIT

export locuszoom4dash

"""
    locuszoom4dash(;kwargs...)

A Locuszoom4Dash component.
Locuszoom4Dash is the DASH version of LocusZoom.js.
It takes ...
Keyword arguments:
- `id` (String; optional): The ID used to identify this component in Dash callbacks
- `data_sources` (Array of Dicts; optional): Definition of the datasrources for this Locuszoom

Format example:
 [{
     name: "assoc",
     data: [
         "AssociationLZ",
         {
             url:  "https://portaldev.sph.umich.edu/api/v1/statistic/single/",
             source: 45,
             id_field: 'variant',
             population: 'ALL',
             build: 'GRCh37'
         }
     ]
 }]
- `layout` (Dict; optional): The layout of the Locuszoom plot.

Either choose from one of the 4 standard layouts, with an optional override,
or define the layout manually.
Example choosing standard layout
{
     'type': 'plot',
     'name': 'standard_association',
     'override': {
         'label_font_size': 20
     }
 }

'type' should always be plot, may be extended in the future
'name' Should be one of ['standard_association','association_catalog','standard_phewas','coaccessibility']
See: https://statgen.github.io/locuszoom/docs/api/module-LocusZoom_Layouts.html for more on layout options
and requirements for the data sources

Example choosing manual layout
{
     'width': 800,
     'panels': [
     {
         'id' : "association",
         'height': 300,
         'data_layers': [
              {
                  'id': "association",
                  'type': "scatter",
                  'x_axis': { field: "assoc:position" },
                  'y_axis': { field: "assoc:log_pvalue" }
              }
         ]
     }
     ]
 }
- `regionChange` (Dict; optional): The change of region, initiated by the user in the LocusZoom plot

Format example: { state: { chr: 6, start: 20379709, end: 20979709 } }
- `state` (Dict; optional): The currently selected region for the LocusZoom plot

Format example: { state: { chr: 6, start: 20379709, end: 20979709 } }
"""
function locuszoom4dash(; kwargs...)
        available_props = Symbol[:id, :data_sources, :layout, :regionChange, :state]
        wild_props = Symbol[]
        return Component("locuszoom4dash", "Locuszoom4Dash", "locuszoom_4_dash", available_props, wild_props; kwargs...)
end

