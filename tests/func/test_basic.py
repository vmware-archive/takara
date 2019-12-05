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
            'path': 'foo/bar/baz',
            'string': 'cheese!',
            }
    await hub.takara.init.create(**kw)
    await hub.takara.init.set(**kw)
    ret = await hub.takara.init.get(**kw)
    assert ret == 'cheese!'
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
            'path': 'foo/bar/baz',
            'file': data_fn,
            }
    await hub.takara.init.create(**kw)
    await hub.takara.init.set(**kw)
    ret = await hub.takara.init.get(**kw)
    assert ret == 'localfile data'
    shutil.rmtree(unit_dir)
    shutil.rmtree(data_dir)
    os.remove(data_fn)


@pytest.mark.asyncio
async def test_file_shamir_string(hub):
    unit_dir = tempfile.mkdtemp()
    data_dir = tempfile.mkdtemp()
    kw = {
            'unit': 'main',
            'seal_raw': '1|ca70a7d491ac716c1c33a4ba445be291fb4d10ae0e2c165ee0ba2edb8a24945b4f2d616b696371715268343d:2|2ab95a231fc95df45b89c1f4d3b8828568066e5a79c5468178083a260866690b4f2d616b696371715268343d:3|92bfaba0bb017cac0b821c01e4b72762f93b17bf2fa46680abf85ccef71bbc254f2d616b696371715268343d:4|62e0f470eccf7375bec402780f46f363eba8b306297716931341520f84351a074f2d616b696371715268343d:5|dae605f34807522deecfdf8d384956847a95cae37f163692c0b134e77b48cf294f2d616b696371715268343d',
            'unit_dir': unit_dir,
            'data_dir': data_dir,
            'store': 'file',
            'cipher': 'fernet',
            'seal': 'shamir',
            'path': 'foo/bar/baz',
            'string': 'cheese!',
            }
    await hub.takara.init.create(**kw)
    await hub.takara.init.set(**kw)
    ret = await hub.takara.init.get(**kw)
    assert ret == 'cheese!'
    shutil.rmtree(unit_dir)
    shutil.rmtree(data_dir)


@pytest.mark.asyncio
async def test_file_shamir_file(hub):
    unit_dir = tempfile.mkdtemp()
    data_dir = tempfile.mkdtemp()
    _, data_fn = tempfile.mkstemp()
    with open(data_fn, 'wb+') as wfh:
        wfh.write(b'localfile data')
    kw = {
            'unit': 'main',
            'unit_dir': unit_dir,
            'data_dir': data_dir,
            'seal_raw': '1|ca70a7d491ac716c1c33a4ba445be291fb4d10ae0e2c165ee0ba2edb8a24945b4f2d616b696371715268343d:2|2ab95a231fc95df45b89c1f4d3b8828568066e5a79c5468178083a260866690b4f2d616b696371715268343d:3|92bfaba0bb017cac0b821c01e4b72762f93b17bf2fa46680abf85ccef71bbc254f2d616b696371715268343d:4|62e0f470eccf7375bec402780f46f363eba8b306297716931341520f84351a074f2d616b696371715268343d:5|dae605f34807522deecfdf8d384956847a95cae37f163692c0b134e77b48cf294f2d616b696371715268343d',
            'store': 'file',
            'cipher': 'fernet',
            'seal': 'shamir',
            'path': 'foo/bar/baz',
            'file': data_fn,
            }
    await hub.takara.init.create(**kw)
    await hub.takara.init.set(**kw)
    ret = await hub.takara.init.get(**kw)
    assert ret == 'localfile data'
    shutil.rmtree(unit_dir)
    shutil.rmtree(data_dir)
    os.remove(data_fn)
