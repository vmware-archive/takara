'''
Functions used to migrate a unit from one store/seal/cipher to another
'''

async def unit(hub, unit, **kw):
    '''
    Migrate the named unit to a new store/seal/cipher
    '''
    if unit not in hub.takara.UNITS:
        raise takara.exc.UnitMissingError('The named unit "{unit}" is not available')
    unit_config = hub.takara.UNITS[unit]
    if kw['store'] == unit_config['store']:
        # Unit stores will collide! Can't do the migration inline

