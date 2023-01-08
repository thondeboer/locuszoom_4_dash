% Auto-generated: do not edit by hand
\name{locuszoom4Dash}

\alias{locuszoom4Dash}

\title{Locuszoom4Dash component}

\description{
Locuszoom4Dash is the DASH version of LocusZoom.js. It takes ...
}

\usage{
locuszoom4Dash(id=NULL, data_sources=NULL, elementSelection=NULL,
layout=NULL, regionChange=NULL, state=NULL)
}

\arguments{
\item{id}{Character. The ID used to identify this component in Dash callbacks}

\item{data_sources}{List of named lists. Definition of the datasrources for this Locuszoom

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
 }]}

\item{elementSelection}{Named list. Element in the plot selected

Format: The element attribute of the LocusZoom data object is returned.
It is not supposed to be edited in Dash, but only used for reporting selections in the LocusZoom plot}

\item{layout}{Named list. The layout of the Locuszoom plot.

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
'name' Should be one of ['standard_association','association_catalog','standard_phewas','coaccessibility','interval_association']
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
 }}

\item{regionChange}{Named list. The change of region, initiated by the user in the LocusZoom plot

Format example: { state: { chr: 6, start: 20379709, end: 20979709 } }}

\item{state}{Named list. The currently selected region for the LocusZoom plot

Format example: { state: { chr: 6, start: 20379709, end: 20979709 } }}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

