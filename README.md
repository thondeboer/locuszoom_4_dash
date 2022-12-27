# Locuszoom 4 DASH

Locuszoom 4 DASH is a Dash component library, based on the [LocusZoom.js package](https://statgen.github.io/locuszoom/docs/api/index.html) for interactively visualizing statistical genetic data from customizable sources .

This version does not expose all of the functionality of LocusZoom.js, but it provdes a great starting point to include LocusZoom in any Dash application.

This is the minimal python code to render a LocusZoom image:

```python
import locuszoom_4_dash

from dash import Dash, callback, html, Input, Output, dcc, State, callback_context
from dash.exceptions import PreventUpdate

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
# This contains many of the data sources from the Samples, but not all plots use all data sources
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

![LocusZoom 4 DASH minimal](https://github.com/thondeboer/locuszoom_4_dash/img/LocusZoom_4_DASH_minimal.png "LocusZoom 4 DASH minimal")

It exposes the ```state``` for the LocusZoom image, which contains the focus of the plot. It allows the user to update the location of the focus from the DASH component. It also allows the user to change the location by dragging the image and it will conversely update the attributes for the components, so Dash callbacks can respond to it.

![LocusZoom 4 DASH full](https://github.com/thondeboer/locuszoom_4_dash/img/LocusZoom_4_DASH_full.gif "LocusZoom 4 DASH full")


Get started with:
1. Install Dash and its dependencies: https://dash.plotly.com/installation
2. Run `python usage.py`
3. Visit http://localhost:8050 in your web browser

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md)

### Install dependencies

If you have selected install_dependencies during the prompt, you can skip this part.

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

### Write your component code in `src/lib/components/Locuszoom4Dash.react.js`.

- The demo app is in `src/demo` and you will import your example component code into your demo app.
- Test your code in a Python environment:
    1. Build your code
        ```
        $ npm run build
        ```
    2. Run and modify the `usage.py` sample dash app:
        ```
        $ python usage.py
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
