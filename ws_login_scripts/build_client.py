""" Utility for packaging the client application to an isolated zip file

This project assumes it is executing in the root of the project
"""

import os
import shutil
import stat
import subprocess as sp
from pathlib import Path



def main():
    build_dir = Path('build/ws_client')
    if build_dir.exists():
        print("Deleteing existing director")
        shutil.rmtree(build_dir)

    if (build_dir.parent / 'ws_client.zip').exists():
        os.remove(build_dir.parent / 'ws_client.zip')


    build_dir.mkdir(parents = True)
    print("Copying files")
    shutil.copytree(Path('ws_login_client'), build_dir / "ws_login_client")
    shutil.copytree(Path('ws_login_domain'), build_dir / "ws_login_domain")
    shutil.copytree(Path('ws_login_ui'), build_dir / "ws_login_ui")

    print("Installing pip dependencies")
    sp.run(['pip', 'install', '--target=' + str(build_dir), 'requests', 'Pillow'])
    
    print("Writting Boot script")
    launch_script = build_dir / 'launch.pyw'
    with open(launch_script, 'w') as f:
        f.write("""#!/bin/env python

import os
import sys
from pathlib import Path

os.environ['API_HOST'] = '{{ API Host goes here }}'
os.environ['API_TOKEN'] = '{{ API toekn goes here }}'
os.environ['POLL_INTERVAL'] = 30 # seconds

script_location = Path(sys.argv[0])

print(script_location)
os.chdir(script_location.parent)

import ws_login_ui 
ws_login_ui.launch()
""");
    # mark file as executable
    os.chmod(launch_script, os.stat(launch_script).st_mode | stat.S_IEXEC)

    print("Compressing Artifact")
    shutil.make_archive(build_dir.parent / 'ws_client', 'zip', build_dir)

    print("Done")

if __name__ == "__main__":
    main()
