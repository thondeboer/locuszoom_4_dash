import React, {Component} from 'react';
import PropTypes from 'prop-types';
import LocuszoomD3 from '../d3/locuszoom';

/**
 * Locuszoom4Dash is the DASH version of LocusZoom.js.
 * It takes ...
 */
export default class Locuszoom4Dash extends Component {

    componentDidMount() {
        this.locuszoom = new LocuszoomD3(this.el, this.props, data => {
            const {setProps} = this.props;
            const regionChange = {regionChange: data.data};

            if (setProps) { setProps(regionChange); }
            else { this.setState({regionChange}); }
        });
    }

    componentDidUpdate() {
        this.locuszoom.update(this.props);
    }

    render() {
        return <div id={this.props.id} ref={el => {this.el = el}}/>;
    }
}

Locuszoom4Dash.defaultProps = {};

Locuszoom4Dash.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks
     */
    id: PropTypes.string,

    /**
     * Dash-assigned callback that should be called whenever any of the
     * properties change
     */
    setProps: PropTypes.func,

    /**
     * The layout of the Locuszoom plot.
     * 
     * Either choose from one of the 4 standard layouts, with an optional override,
     * or define the layout manually.
     * Example choosing standard layout
     * {
     *      'type': 'plot',
     *      'name': 'standard_association',
     *      'override': {
     *          'label_font_size': 20
     *      }
     *  }
     * 
     * 'type' should always be plot, may be extended in the future
     * 'name' Should be one of ['standard_association','association_catalog','standard_phewas','coaccessibility']
     * See: https://statgen.github.io/locuszoom/docs/api/module-LocusZoom_Layouts.html for more on layout options
     * and requirements for the data sources
     * 
     * Example choosing manual layout
     * {
     *      'width': 800,
     *      'panels': [
     *      {
     *          'id' : "association",
     *          'height': 300,
     *          'data_layers': [
    *               {
    *                   'id': "association",
    *                   'type': "scatter",
    *                   'x_axis': { field: "assoc:position" },
    *                   'y_axis': { field: "assoc:log_pvalue" }
    *               }
     *          ]
      *      }
     *      ]
     *  }
     * 
     * 
     */
    layout: PropTypes.object,

    /**
     * Definition of the datasrources for this Locuszoom
     * 
     * Format example:
     *  [{
     *      name: "assoc",
     *      data: [
     *          "AssociationLZ",
     *          {
     *              url:  "https://portaldev.sph.umich.edu/api/v1/statistic/single/",
     *              source: 45,
     *              id_field: 'variant',
     *              population: 'ALL',
     *              build: 'GRCh37'
     *          }
     *      ]
     *  }]
     * 
     * 
     */
    data_sources: PropTypes.arrayOf(PropTypes.object),

    /**
     * The currently selected region for the LocusZoom plot
     * 
     * Format example: { state: { chr: 6, start: 20379709, end: 20979709 } }
     */
    state: PropTypes.object,

    /**
     * The change of region, initiated by the user in the LocusZoom plot
     * 
     * Format example: { state: { chr: 6, start: 20379709, end: 20979709 } }
     */
    regionChange: PropTypes.object,
};

