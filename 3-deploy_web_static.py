#!/usr/bin/python3
"""creates and distributes an archive to your web servers"""

from fabric.api import local, run, put
from datetime import datetime
from os import path


def do_pack():
    """Generates a tgz archive"""

    try:
        file_time = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = "web_static_{}.tgz".format(file_time)
        comm = "tar -cvzf versions/{} web_static".format(file_name)
        local("mkdir -p versions")
        return local(comm)
    except:
        return None


def do_deploy(archive_path):
    """distributes an archive to your web servers"""

    if path.exists(archive_path) is True:
        try:
            path_ls = archive_path.split("/")
            file_name = path_ls[-1]
            name_no_ext = file_name.split(".")[0]
            p = "/data/web_static/releases/"
            put(archive_path, '/tmp/')
            run('mkdir -p {}{}/'.format(p, name_no_ext))
            run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, p, name_no_ext))
            run('rm /tmp/{}'.format(file_name))
            run('mv {}{}/web_static/* {}{}/'.format(p, name_no_ext,
                                                    p, name_no_ext))
            run('rm -rf {}{}/web_static'.format(p, name_no_ext))
            run('rm -rf /data/web_static/current')
            run('ln -s {}{}/ /data/web_static/current'.format(p, name_no_ext))
            return True
        except:
            return False
    return False


def deploy():
    """creates and distributes an archive to your web server"""
    path = do_pack()
    if path is None:
        return False
    return do_deploy(path)
