import logging

logger = logging.getLogger('upgrade')


def migrate(cr, version):
    if version is None:
        return
    logger.info("Migrating mgmtsystem_audit from version %s", version)
    logger.info("Updating state flags")
    cr.execute("update mgmtsystem_audit set state = 'open' where state = 'o'")
    cr.execute("update mgmtsystem_audit set state = 'done' where state = 'c'")
    logger.info("mgmtsystem_audit update... done!")
