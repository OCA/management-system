def init_pools(ctx):
    """
    Init some model from the pool for the tests.

    Shortcut available for all tests for models that
    are more likely going to be used in the tests.
    """
    ctx.asset_category = ctx.registry("mgmtsystem.security.assets.category")
    ctx.asset_essential = ctx.registry("mgmtsystem.security.assets.essential")
    ctx.asset_underlying = ctx.registry("mgmtsystem."
                                        "security.assets.underlying")

    ctx.event = ctx.registry("mgmtsystem.security.event")
    ctx.event_measure = ctx.registry("mgmtsystem.security.event.measure")
    ctx.event_scenario = ctx.registry("mgmtsystem.security.event.scenario")

    ctx.security_measure = ctx.registry("mgmtsystem.security.measure")

    ctx.threat_origin = ctx.registry("mgmtsystem.security.threat.origin")
    ctx.threat_scenario = ctx.registry("mgmtsystem.security.threat.scenario")

    ctx.severity = ctx.registry('mgmtsystem.severity')
    ctx.probability = ctx.registry('mgmtsystem.probability')
