# Locuszoom 4 DASH

Locuszoom 4 DASH is a Dash component library, based on the [LocusZoom.js package](https://statgen.github.io/locuszoom/docs/api/index.html) for interactively visualizing statistical genetic data from customizable sources.

This version does not expose all of the functionality of LocusZoom.js, but it provdes a great starting point to include LocusZoom in any Dash application.

![LocusZoom 4 DASH minimal](https://github.com/thondeboer/locuszoom_4_dash/raw/master/img/LocusZoom_4_DASH_minimal.png "LocusZoom 4 DASH minimal")

This is the minimal python code to render a LocusZoom image:

```python
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
```

It exposes the ```state``` for the LocusZoom image, which contains the focus of the plot. It allows the user to update the location of the focus from the DASH component. It also allows the user to change the location by dragging the image and/or zooming in/out and it will conversely update the properties for the components, so Dash callbacks can respond to it.

![LocusZoom 4 DASH full](https://github.com/thondeboer/locuszoom_4_dash/raw/master/img/LocusZoom_4_DASH_full.gif "LocusZoom 4 DASH full")

See the file [examples/usage.py](https://github.com/thondeboer/locuszoom_4_dash/blob/master/usage.py) for the source code for the App in the GIF.

## Update on Jan 2023

Some additional functionality was added to the component allowing for adding and changing panels, adding trackInfo and reacting to more events on the LocusZoom plot.

![LocusZoom 4 DASH Update](https://github.com/thondeboer/locuszoom_4_dash/raw/master/img/LocusZoom_4_DASH_UpdateJan2023.gif "LocusZoom 4 DASH Update Jan 2023")
### Added functionality
1. The Dash component can now react to events in the Locuszoom plot, such as selection of points on the plots, regions or genes.
    * The examples will show the information that is captured in the event in a ```Pre``` component but is in essence the ```element``` property of the component.
    * The exception is for the ```genes``` track. The ```transcripts``` property that contains a full list of all the isoforms of the gene is NOT exported to the Dash component, since it is a circular construct (each transcript has as its child also a gene, which has transcripts, etc.). The canonical transcript information IS provided in the ```element``` since that does not have a circular construct.
    * For the same reason, the ```element``` does also not contain the ```parents``` property.
1. Tracks can now show ```trackInfo``` field in a drop down to provide the user with more information about the track.
    * The track info will be constructed from the ```dataInfo``` property of the ```data_source``` definition
    * The track info will be rendered as HTML, so the ```dataInfo``` property can contain standard HTML markup
    * Example: ```'dataInfo': f"<strong>GWAS study: 45</strong><br>Build: {BUILD}"```
1. Panels can be added to the standard plot layouts with the ```addPanel``` property in the ```layout``` property
    * In the ```layout``` property you can define a ```addPanel``` property which is a list of objects
    * Each object contains two properties; ```name``` and ```overrides``` which correspond to the values in the ```LocusZoom.Layouts.get()``` method
    * See the [Layouts and Visualization Options](https://statgen.github.io/locuszoom/docs/guides/rendering_layouts.html) page for more on adding panels to a layout
1. A standard layout can be changed using the ```LocusZoom.Layouts.mutate_attrs``` method"
    * In the ```layout``` property, you can define a ```mutate_attrs``` property which is a list of objects
    * Each object, contains two properties; ```jsonpath``` and ```setval``` that corresponds to the two parameters for the ```LocusZoom.Layouts.mutate_attrs``` method
        * In case the ```setval``` needs to be a full javascript function, enclose it in triple quotes as shown below
        * Internally, this is using an ```eval``` method to parse the string into proper Javascript and while this is usually not recommended, it is up to the user to ensure nothing "evil" is being done with the ```eval```!
    * See more in the [Guide to interactivity](https://statgen.github.io/locuszoom/docs/guides/interactivity.html) on the official LocusZoom page on the usage

Here are some examples:

Since the GWASCatalog is only 50px high, the trackInfo menu does not render properly. To adjust the height, using the following as a ```mutate``` property in the layout definition:

```python
        layout={
            'type':'plot',
            'name':'association_catalog',
            'override': {
                'max_region_scale': max_region_scale,
                'min_region_scale': min_region_scale,
            },
            'mutate_attrs': [
                {
                    'jsonpath': '$..panels[?(@.tag === "gwascatalog")].height',
                    'setval': 75
                },
            ]
        },
```

Here's an example to always show the Intervals legend:

```python
...
        layout={
            'type':'plot',
            'name':'interval_association',
            'override': {
                'max_region_scale': max_region_scale,
                'min_region_scale': min_region_scale,
            },
            'mutate_attrs': [
                {
                    'jsonpath': '$..panels[?(@.tag === "intervals")].legend.hidden',
                    'setval': False
                },
                {
                    'jsonpath': '$..data_layers[?(@.tag === "intervals")].always_hide_legend',
                    'setval': False
                },
            ]
        },
...
```

This example shows the addition of the intervals panel to the standard association_catalog panel:

```python
...

        layout={
            'type':'plot',
            'name':'association_catalog',
            'override': {
                'max_region_scale': max_region_scale,
                'min_region_scale': min_region_scale,
            },
            # See https://statgen.github.io/locuszoom/docs/api/module-LocusZoom_Layouts.html for name of panels
            'addPanel': [
                {
                    'name': 'intervals',
                    'overrides': {
                        'height': 100
                    }
                }
            ],
...
```

This examples shows a more complex modification, requireing a small piece of Javascript code. It is encapsulated in thriple quotes and will be ```eval```uated as Javascript. The code modifies the default PheWas plot, to show a line on the gene panel, showing the location of the variant.

```python
...
        layout={
            'type':'plot',
            'name':'standard_phewas',
            'override': {
                'max_region_scale': max_region_scale,
                'min_region_scale': min_region_scale,
            },
            'mutate_attrs': [
                {
                    'jsonpath': '$..panels[?(@.tag === "genes")].data_layers',
                    'setval': """
                        (old_layers) => {
                            var VARIANT_PATTERN = /(\d+):(\d+)_([ATGC])\/([ATGC])/;
                            var variantGroups = VARIANT_PATTERN.exec(figure.state.variant);
                            var variantPosition = Number(variantGroups[2]);
                            old_layers.push(
                                {
                                    id: "variant",
                                    type: "orthogonal_line",
                                    orientation: "vertical",
                                    offset: variantPosition,
                                    style: {
                                        "stroke": "#FF3333",
                                        "stroke-width": "2px",
                                        "stroke-dasharray": "4px 4px"
                                    }
                                }
                            );
                            return old_layers;
                        }
                    """
                },
            ]
        },
...

```
# Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md)

### Install dependencies

These are required for the further development of the component.

1. Install npm packages
    ```
    $ npm install
    ```
2. Create a virtual env and activate.
    ```
    $ virtualenv venv
    $ . venv/bin/activate
    ```
    _Note: venv\Scripts\activate for windows_

3. Install python packages required to build components.
    ```
    $ pip install -r requirements.txt
    ```
4. Install the python packages for testing (optional)
    ```
    $ pip install -r tests/requirements.txt
    ```

### The component code is in `src/lib/components/Locuszoom4Dash.react.js`.

- Test your code in a Python environment:
    1. Build your code
        ```
        $ npm run build
        ```
    2. Run and modify the `usage.py` sample dash app:
        ```
        $ python examples/usage.py
        ```
- Write tests for your component.
    - A sample test is available in `tests/test_usage.py`, it will load `usage.py` and you can then automate interactions with selenium.
    - Run the tests with `$ pytest tests`.
    - The Dash team uses these types of integration tests extensively. Browse the Dash component code on GitHub for more examples of testing (e.g. https://github.com/plotly/dash-core-components)
- Add custom styles to your component by putting your custom CSS files into your distribution folder (`locuszoom_4_dash`).
    - Make sure that they are referenced in `MANIFEST.in` so that they get properly included when you're ready to publish your component.
    - Make sure the stylesheets are added to the `_css_dist` dict in `locuszoom_4_dash/__init__.py` so dash will serve them automatically when the component suite is requested.
- [Review your code](./review_checklist.md)

### Create a production build and publish:

1. Build your code:
    ```
    $ npm run build
    ```
2. Create a Python distribution
    ```
    $ python setup.py sdist bdist_wheel
    ```
    This will create source and wheel distribution in the generated the `dist/` folder.
    See [PyPA](https://packaging.python.org/guides/distributing-packages-using-setuptools/#packaging-your-project)
    for more information.

3. Test your tarball by copying it into a new environment and installing it locally:
    ```
    $ pip install locuszoom_4_dash-0.7.0.tar.gz
    ```

4. If it works, then you can publish the component to NPM and PyPI:
    1. Publish on PyPI
        ```
        $ twine upload dist/*
        ```
    2. Cleanup the dist folder (optional)
        ```
        $ rm -rf dist
        ```
    3. Publish on NPM (Optional if chosen False in `publish_on_npm`)
        ```
        $ npm publish
        ```
        _Publishing your component to NPM will make the JavaScript bundles available on the unpkg CDN. By default, Dash serves the component library's CSS and JS locally, but if you choose to publish the package to NPM you can set `serve_locally` to `False` and you may see faster load times._

5. Share your component with the community! https://community.plotly.com/c/dash
    1. Publish this repository to GitHub
    2. Tag your GitHub repository with the plotly-dash tag so that it appears here: https://github.com/topics/plotly-dash
    3. Create a post in the Dash community forum: https://community.plotly.com/c/dash
