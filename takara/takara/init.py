__func_alias__ = {'set_': 'set'}


def __init__(hub):
    hub.pop.sub.load_subdirs(hub.takara)
    hub.takara.UNITS = {}


def cli(hub):
    '''
    Start the direct cli interface for takara
    '''
    hub.pop.conf.integrate(['takara'], cli='takara', loader='yaml', roots=True)
    kw = hub.OPT['takara']
    hub.pop.loop.start(hub.takara.init.start(**kw))


async def start(hub, **kw):
    await hub.takara.init.setup(**kw)
    coro = {'create': hub.takara.init.create,
     'set': hub.takara.init.set,
     'get': hub.takara.init.get}[hub.OPT['_subparser_']](**kw)
    print(await coro)


async def setup(hub, **kw):
    '''
    Given the store and the kwargs to access the given store
    '''
    store = kw['store']
    await getattr(hub, f'takara.store.{store}.config')(**kw)


async def create(hub, **kw):
    '''
    Set up the environment based on the available data
    '''
    cipher = kw['cipher']
    seal = kw['seal']
    store = kw['store']
    kw['seal_raw'] = await getattr(hub, f'takara.seal.{seal}.gen')()
    kw['seal_data'] = await getattr(hub, f'takara.seal.{seal}.create')(**kw)
    return await getattr(hub, f'takara.store.{store}.create')(**kw)


async def unseal(hub, **kw):
    '''
    Unseal the desired unit.
    '''
    unit = kw['unit']
    unit_config = hub.takara.UNITS[unit]
    seal = unit_config['seal']
    cipher = unit_config['cipher']
    seal_data = unit_config['seal_data']
    if kw.get('seal_raw'):
        seal_raw = kw['seal_raw']
    else:
        seal_raw = await getattr(hub, f'takara.seal.{seal}.gen')(kw.get('passwd', None))
    if not await getattr(hub, f'takara.seal.{seal}.verify')(seal_raw, seal_data):
        return False
    await getattr(hub, f'takara.cipher.{cipher}.setup')(unit, seal_raw)
    return True


async def set_(hub, **kw):
    '''
    Set a specific value to a specific path
    '''
    if kw['unit'] not in hub.takara.UNITS:
        raise takara.exc.UnitMissingError()
    unit = kw['unit']
    unit_config = hub.takara.UNITS[unit]
    cipher = unit_config['cipher']
    store = unit_config['store']
    # TODO: If we need to add data sources make this a sub
    if kw.get('file'):
        with open(kw['file'], 'rb') as rfh:
            data = rfh.read()
    elif kw.get('string'):
        data = kw['string'].encode('utf-8')
    unsealed = await hub.takara.init.unseal(**kw)
    if not unsealed:
        raise takara.exc.UnsealError('Falied to unseal the treasure, was entry correct?')
    enc = await getattr(hub, f'takara.cipher.{cipher}.encrypt')(unit, data)
    await getattr(hub, f'takara.store.{store}.set')(unit, kw['path'], enc)


async def get(hub, **kw):
    '''
    Set a specific value to a specific path
    '''
    if kw['unit'] not in hub.takara.UNITS:
        raise takara.exc.UnitMissingError()
    unit = kw['unit']
    unit_config = hub.takara.UNITS[unit]
    cipher = unit_config['cipher']
    store = unit_config['store']
    unsealed = await hub.takara.init.unseal(**kw)
    if not unsealed:
        raise takara.exc.UnsealError('Falied to unseal the treasure, was entry correct?')
    enc = await getattr(hub, f'takara.store.{store}.get')(unit, kw['path'])
    return await getattr(hub, f'takara.cipher.{cipher}.decrypt')(unit, enc)
