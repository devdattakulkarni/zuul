import json
import gearman
import uuid


class ZuulData(object):
    def __init__(self, gearman_data):
        args = json.loads(gearman_data)
        self.uuid = args['ZUUL_UUID']
        """Zuul provided key to link builds with Gerrit events"""

        self.ref = args['ZUUL_REF']
        """Zuul provided ref that includes commit(s) to build"""

        self.commit = args['ZUUL_COMMIT']
        """The commit SHA1 at the head of ZUUL_REF"""

        self.project = args['ZUUL_PROJECT']
        """The project that triggered this build"""

        self.pipeline = args['ZUUL_PIPELINE']
        """The Zuul pipeline that is building this job"""

        self.zuul_url = args['ZUUL_URL']
        """The url for the zuul server as configured in zuul.conf"""

        if 'ZUUL_BRANCH' in args:
            self.branch = args['ZUUL_BRANCH']
            """The target branch for the change that triggered this build"""


def task_listener_git_update(gearman_worker, gearman_job):
    name = 'build:foo-git-update'
    number = str(uuid.uuid4())
    manager = 'solum_job_manager'
    data = ZuulData(gearman_job.data)
    gearman_worker.send_job_data(gearman_job,
                                 json.dumps(dict(name=name,
                                                 number=number,
                                                 manager=manager)))
    gearman_worker.send_job_status(gearman_job, 0, 100)
    print data    # do stuff
    gearman_worker.send_job_status(gearman_job, 100, 100)
    gearman_worker
    return 'SUCCESS'


gm_worker = gearman.GearmanWorker(['localhost:4730'])
gm_worker.register_task('build:foo-git-update', task_listener_git_update)
#gm_worker.register_task('build:foo-lp-build', task_listener_reverse_inflight)
gm_worker.work()
