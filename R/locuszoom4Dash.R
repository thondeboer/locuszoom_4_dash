# AUTO GENERATED FILE - DO NOT EDIT

#' @export
locuszoom4Dash <- function(id=NULL, data_sources=NULL, layout=NULL, regionChange=NULL, state=NULL) {
    
    props <- list(id=id, data_sources=data_sources, layout=layout, regionChange=regionChange, state=state)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'Locuszoom4Dash',
        namespace = 'locuszoom_4_dash',
        propNames = c('id', 'data_sources', 'layout', 'regionChange', 'state'),
        package = 'locuszoom4Dash'
        )

    structure(component, class = c('dash_component', 'list'))
}
