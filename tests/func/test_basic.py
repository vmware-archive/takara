# Import python libs
import tempfile
import shutil
import os
# Import third party libs
import pytest


@pytest.mark.asyncio
async def test_file_passwd_string(hub):
    unit_dir = tempfile.mkdtemp()
    data_dir = tempfile.mkdtemp()
    kw = {
            'unit': 'main',
            'seal_raw': 'foobar',
            'unit_dir': unit_dir,
            'data_dir': data_dir,
            'store': 'file',
            'cipher': 'fernet',
            'seal': 'passwd',
            'path': 'foo.bar.baz',
            'string': 'cheese!',
            }
    await hub.takara.init.create(**kw)
    await hub.takara.init.set(**kw)
    ret = await hub.takara.init.get(**kw)
    assert ret == b'cheese!'
    shutil.rmtree(unit_dir)
    shutil.rmtree(data_dir)


@pytest.mark.asyncio
async def test_file_passwd_file(hub):
    unit_dir = tempfile.mkdtemp()
    data_dir = tempfile.mkdtemp()
    _, data_fn = tempfile.mkstemp()
    with open(data_fn, 'wb+') as wfh:
        wfh.write(b'localfile data')
    kw = {
            'unit': 'main',
            'seal_raw': 'foobar',
            'unit_dir': unit_dir,
            'data_dir': data_dir,
            'store': 'file',
            'cipher': 'fernet',
            'seal': 'passwd',
            'path': 'foo.bar.baz',
            'file': data_fn,
            }
    await hub.takara.init.create(**kw)
    await hub.takara.init.set(**kw)
    ret = await hub.takara.init.get(**kw)
    assert ret == b'localfile data'
    shutil.rmtree(unit_dir)
    shutil.rmtree(data_dir)
    os.remove(data_fn)