import logging
from oslo.config import cfg
from oslo import messaging

class Client(object):
    log = logging.getLogger("zuul.messaging.client")

    def __init__(self):
        transport = messaging.get_transport(cfg.CONF, url='rabbit://guest:password@localhost')
        target = messaging.Target(topic='zuul', server='trigger')
        self._client = messaging.RPCClient(transport, target)

    def trigger(self, ctxt, arg):
        cctxt = self._client.prepare(timeout=10)
        return cctxt.call(ctxt, 'trigger', arg=arg)

c = Client()
print c.trigger({}, dict(event_type='ref-updated', project_name='solum/foo', branch='master', ref='refs/remotes/origin/master',
                         newrev='14ff03b47afe91a47fe7e327266f1035fd52ffdc', oldrev='060639e2d2e976570b47e3ebcc9b2ffa83c3fdd4'))