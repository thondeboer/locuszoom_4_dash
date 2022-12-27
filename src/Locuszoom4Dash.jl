
module Locuszoom4Dash
using Dash

const resources_path = realpath(joinpath( @__DIR__, "..", "deps"))
const version = "0.0.1"

include("jl/locuszoom4dash.jl")

function __init__()
    DashBase.register_package(
        DashBase.ResourcePkg(
            "locuszoom_4_dash",
            resources_path,
            version = version,
            [
                DashBase.Resource(
    relative_package_path = "locuszoom_4_dash.min.js",
    external_url = "https://unpkg.com/locuszoom_4_dash@0.0.1/locuszoom_4_dash/locuszoom_4_dash.min.js",
    dynamic = nothing,
    async = nothing,
    type = :js
),
DashBase.Resource(
    relative_package_path = "locuszoom_4_dash.min.js.map",
    external_url = "https://unpkg.com/locuszoom_4_dash@0.0.1/locuszoom_4_dash/locuszoom_4_dash.min.js.map",
    dynamic = true,
    async = nothing,
    type = :js
)
            ]
        )

    )
end
end
