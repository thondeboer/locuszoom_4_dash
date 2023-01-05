import LocusZoom from 'locuszoom';

export default class LocuszoomD3 {
    constructor(el, figure, onRegionChange) {
        const self = this;
        self.update = self.update.bind(self);
        self.state =  figure.state;

        const data_sources = new LocusZoom.DataSources();
        for(let i = 0; i < figure.data_sources.length; i++) {
            data_sources.add(figure.data_sources[i].name, figure.data_sources[i].data);
        }
        
        // Check if we want named plots with optional override
        let layout;
        if (figure.layout.type && figure.layout.name) {
            const override = Object.assign({}, figure.layout.override, {state: figure.state});
            layout = LocusZoom.Layouts.get(figure.layout.type, figure.layout.name, override);
            // Adding the vertical line to the standard_phewas layout
                if (figure.layout.name === 'standard_phewas') {
                    // Break the variant into constituent parts for setting plot state
                    var VARIANT_PATTERN = /(\d+):(\d+)_([ATGC])\/([ATGC])/;
                    var variantGroups = VARIANT_PATTERN.exec(figure.state.variant);
                    var variantPosition = Number(variantGroups[2]);
                    LocusZoom.Layouts.mutate_attrs(layout, '$.panels[?(@.tag === "genes")].data_layers', (old_layers) => old_layers.concat([{
                    id: "variant",
                    type: "orthogonal_line",
                    orientation: "vertical",
                    offset: variantPosition,
                    style: {
                      "stroke": "#FF3333",
                      "stroke-width": "2px",
                      "stroke-dasharray": "4px 4px"
                    }
                  }]));
                }
        } else {
            // TODO Check if layout is proper layout
            layout = figure.layout;
        }
        // Generate the LocusZoom plot
        self.plot = LocusZoom.populate(el, data_sources, layout);
        // Register the callback hook (?) when a region has changed
        self.onRegionChange = self.plot.on('region_changed', onRegionChange);
    }

    // figure simply represents all the properties of the LocusZoom object (figure === this.props)
    // BUT we only update the figure when the STATE (selected region) is updated
    update(figure) {
        const self = this;
        if (!(Object.is(self.state, figure.state)) ) {
            self.state = figure.state;
            self.plot.applyState(figure.state);
        }
    };
};