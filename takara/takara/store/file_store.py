'''
Create a unit storage system based on a local file directory
'''
# Import python libs
import os
import shutil
# Import third party libs
import msgpack
# Import local libs
import takara.exc

__virtualname__ = 'file'
__func_alias__ = {'set_': 'set', 'list_': 'list'}
UNIT_FN = 'config.mp'


async def config(hub, data_dir):
    '''
    Get the existing configuration for all available unit files
    '''
    ret = {}
    data_dir = data_dir
    for unit_name in os.listdir(data_dir):
        unit_file = os.path.join(data_dir, unit_name, UNIT_FN)
        if os.path.isfile(unit_file):
            with open(unit_file, 'rb') as rfh:
                ret[unit_name] = msgpack.loads(rfh.read(), raw=False)
    hub.takara.UNITS.update(ret)


async def create(hub, **kw):
    '''
    Given a directory to create the store in, make the root directory used
    for the store adn place the unit confiruration inside.
    '''
    data_dir = kw['data_dir']
    unit_name = kw['unit']
    unit_root = os.path.join(kw['unit_dir'], unit_name)
    cipher = kw['cipher']
    seal = kw['seal']
    seal_data = kw['seal_data']
    unit_dir = os.path.join(data_dir, unit_name)
    unit_file = os.path.join(unit_dir, UNIT_FN)
    if os.path.isfile(unit_file):
        raise takara.exc.UnitExistsError(f'Unit "{unit_name}" exists and is defined in file "{unit_file}", either delete this unit or chose another name')
    if not os.path.isdir(unit_dir):
        os.makedirs(unit_dir)
    if not os.path.isdir(unit_root):
        os.makedirs(unit_root)
    data = {'cipher': cipher,
            'seal': seal,
            'unit_root': unit_root,
            'seal_data': seal_data,
            'store': 'file',
            'unit_file': unit_file,
            }
    old_umask = os.umask(54)
    with open(unit_file, 'wb+') as wfh:
        wfh.write(msgpack.dumps(data, use_bin_type=True))
    os.umask(old_umask)
    # refresh the unit config on the hub
    await hub.takara.store.file.config(data_dir=data_dir)


async def set_(hub, unit, path, value):
    '''
    Given the named unit, set the named value. The value should already be
    encrypted using the named unit's sealing mechanism
    '''
    if unit not in hub.takara.UNITS:
        raise takara.exc.UnitMissingError('The named unit "{unit}" is not available')
    unit_config = hub.takara.UNITS[unit]
    unit_root = unit_config['unit_root']
    fn_path = os.path.join(unit_root, path.replace('.', os.sep))
    fn_dir = os.path.dirname(fn_path)
    if not os.path.isdir(fn_dir):
        os.makedirs(fn_dir)
    old_umask = os.umask(54)
    with open(fn_path, 'wb+') as wfh:
        wfh.write(value)
    os.umask(old_umask)


async def get(hub, unit, path):
    '''
    Given the unit name and the path, get the encrypted data from the given path
    '''
    if unit not in hub.takara.UNITS:
        raise takara.exc.UnitMissingError('The named unit "{unit}" is not available')
    unit_config = hub.takara.UNITS[unit]
    unit_root = unit_config['unit_root']
    fn_path = os.path.join(unit_root, path.replace('/', os.sep))
    if not os.path.isfile(fn_path):
        raise takara.exc.PathMissingError('The named path "{path}" is not present in unit "{unit}"')
    with open(fn_path, 'rb') as rfh:
        return rfh.read()


async def rm(hub, unit, path):
    '''
    Remove the given path from the system
    '''
    if unit not in hub.takara.UNITS:
        raise takara.exc.UnitMissingError('The named unit "{unit}" is not available')
    unit_config = hub.takara.UNITS[unit]
    unit_root = unit_config['unit_root']
    fn_path = os.path.join(unit_root, path.replace('/', os.sep))
    if os.path.isfile(fn_path):
        os.remove(fn_path)
    elif os.path.isdir(fn_path):
        shutil.rmtree(fn_path)


async def list_(hub, unit, path='/'):
    '''
    List all of the values in a given path location
    '''
    ret = []
    if unit not in hub.takara.UNITS:
        raise takara.exc.UnitMissingError('The named unit "{unit}" is not available')
    unit_config = hub.takara.UNITS[unit]
    unit_root = unit_config['unit_root']
    fn_path = os.path.join(unit_root, path.replace('/', os.sep))
    for root, dirs, files in os.walk(fn_path):
        rel_root = os.relpath(root, fn_path)
        for fn in files:
            ret.append(os.path.join(rel_root, fn))
    return ret


async def rm_unit(hub, unit):
    '''
    Remove the named unit from the system
    '''
    if unit not in hub.takara.UNITS:
        raise takara.exc.UnitMissingError('The named unit "{unit}" is not available')
    unit_config = hub.takara.UNITS.pop(unit)
    shutil.rmtree(unit_config['unit_root'])
    os.remove(unit_config['unit_file'])


async def rename_unit(hub, unit, new_unit):
    '''
    Take the given unit and rename it
    '''
    if unit not in hub.takara.UNITS:
        raise takara.exc.UnitMissingError('The named unit "{unit}" is not available')
    if new_unit in hub.takara.UNITS:
        raise takara.exc.UnitExistsError(f'Unit "{new_unit}" exists, please define another name')
    unit_config = hub.takara.UNITS.pop(unit)
    unit_root = unit_config['unit_root']
    unit_dir = os.path.dirname(unit_root)
    unit_tgt = os.path.join(unit_dir, new_unit)
    unit_file = unit_config['unit_file']
    unit_data_dir = os.path.dirname(unit_file)
    data_dir = os.path.dirname(os.path.dirname(unit_file))
    new_data_dir = os.path.join(data_dir, new_unit)
    new_unit_file = os.path.join(new_data_dir, UNIT_FN)
    if not os.path.isdir(new_data_dir):
        os.makedirs(new_data_dir)
    unit_config['unit_root'] = unit_tgt
    shutil.move(unit_root, unit_tgt)
    with open(new_unit_file, 'wb+') as wfh:
        wfh.write(msgpack.dumps(unit_config, use_bin_type=True))
    await hub.takara.store.file.config(data_dir=data_dir)
    shutil.rmtree(unit_data_dir)
