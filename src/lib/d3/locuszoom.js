import LocusZoom from 'locuszoom';
// Always assume we are using the Intervals extension, even if not used
import IntervalsTrack from 'locuszoom/esm/ext/lz-intervals-track';
import { deepCopy } from 'locuszoom/esm/helpers/layouts';
import { toolbar } from 'locuszoom/esm/layouts';

LocusZoom.use(IntervalsTrack);

export default class LocuszoomD3 {
    constructor(el, figure, onRegionChange, OnElementSelection) {
        const self = this;
        self.update = self.update.bind(self);
        self._createPlot = self._createPlot.bind(self);
        self.state = figure.state;
        self.layout = figure.layout;
        self.el = el;

        self.data_sources = new LocusZoom.DataSources();
        for (let i = 0; i < figure.data_sources.length; i++) {
            self.data_sources.add(figure.data_sources[i].name, figure.data_sources[i].data);
        };
        self.plot = self._createPlot(el, figure);

        // Register the callback hook when a region has changed or something has been selected/clicked
        self.onRegionChange = self.plot.on('region_changed', onRegionChange);
        self.OnElementSelection = self.plot.on('element_selection', OnElementSelection);
        // self.anyEvent = self.plot.on('any_lz_event', (e) => console.log(e));
    };

    _createPlot(el, figure) {
        const self = this;
        // Check if we want named (modified) plots with optional override
        let layout;
        if (figure.layout.type && figure.layout.name) {
            const override = Object.assign({}, figure.layout.override, { state: figure.state });
            layout = this.getLayout(figure.layout.type, figure.layout.name, override)
        } else {
            // TODO Check if layout is proper layout
            layout = figure.layout;
        }

        // Now check if we havesome extra mutation to apply to the layouts
        if (figure.layout.mutate_attrs) {
            for (const mutation of figure.layout.mutate_attrs) {
                LocusZoom.Layouts.mutate_attrs(layout, mutation.jsonpath, eval(mutation.setval));
            }
        }

        // Generate the LocusZoom plot
        return LocusZoom.populate(el, self.data_sources, layout);
    }

    // figure simply represents all the properties of the LocusZoom object (figure === this.props)
    // BUT we only update the figure when the STATE (selected region) is updated
    // TODO Consider updating the layout in Dash and re-render the plot
    // Does not seem that you can update the layout, once created...
    update(figure) {
        const self = this;
        if (!(Object.is(self.state, figure.state))) {
            self.state = figure.state;
            self.plot.applyState(figure.state);
        }
    };

    getLayout(layoutType, layoutName, layoutOverride) {
        // Layout docs: https://statgen.github.io/locuszoom/docs/api/layouts_index.js.html
        const self = this;
        var layout;
        layout = LocusZoom.Layouts.get(layoutType, layoutName, layoutOverride);

        // Check if we have any additional panels to add
        if (self.layout.addPanel) {
            for (const panel of self.layout.addPanel) {
                layout.panels.push(LocusZoom.Layouts.get('panel', panel.name, panel.overrides))
            }
        }

        // Add dataInfo to the panel, if defined in the data source
        for (const panel of layout.panels) {
            var dataInfos = [];
            for (const layer of panel.data_layers) {
                if (layer.namespace) {
                    for (const ns of Object.keys(layer.namespace)) {
                        const dInfo = self.data_sources.get(ns)._config.dataInfo;
                        if (dInfo) { dataInfos.push(dInfo) };
                    }
                }
            }
            // Add the trackInfo meno to the toolbar, if there is any
            if (dataInfos) {
                if (panel.toolbar) {
                    panel.toolbar.widgets.push({
                        type: "menu",
                        color: "yellow",
                        position: "right",
                        button_html: "Track Info",
                        menu_html: dataInfos.join('<br>')
                    })
                } else {
                    const base = deepCopy(toolbar.standard_panel);
                    base.widgets.push({
                        type: "menu",
                        color: "yellow",
                        position: "right",
                        button_html: "Track Info",
                        menu_html: dataInfos.join('<br>')
                    });
                    panel.toolbar = base;
                }
            }
        }
        return layout
    };

}