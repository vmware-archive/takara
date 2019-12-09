'''
Functions used to migrate a unit from one store/seal/cipher to another
'''

async def unit(hub, unit, new_unit, **kw):
    '''
    Migrate the named unit to a new store/seal/cipher
    '''
    if unit not in hub.takara.UNITS:
        raise takara.exc.UnitMissingError('The named unit "{unit}" is not available')
    unit_config = hub.takara.UNITS[unit]
    if kw.get('store', unit_config['store']) == unit_config['store']:
        # Unit stores will collide! Run rename
        await getattr(hub, f'takara.store.{kw["store"]}.rename_unit')(unit, new_unit)


async def seal(hub, unit, seal, seal_raw):
    '''
    Migrate the given unit to a new seal type. This will require re-encrypting
    all data against the new seal.
    '''
    if unit not in hub.takara.UNITS:
        raise takara.exc.UnitMissingError('The named unit "{unit}" is not available')
    unit_config = hub.takara.UNITS[unit]

    # Make temp unit
    # Copy all paths with new seal to tmp unit
    # RM original unit
    # Move tmp unit to orig name
