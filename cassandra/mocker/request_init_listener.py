# -*- coding: utf-8 -*-
import pprint
pp = pprint.PrettyPrinter(indent=4)
from cassandra.cluster import Cluster
from greplin import scales


class RequestAnalyzer(object):
    """
    Used to track request and error counts for a Session.
    Also computes statistics on encoded request size.
    """

    requests = scales.PmfStat('request size')
    errors = scales.IntStat('errors')

    def __init__(self, session):
        scales.init(self, '/cassandra')
        # Each instance will be registered with a session, and receive a callback for each request generated.
        session.add_request_init_listener(self.on_request)

    def on_request(self, rf):
        # This callback is invoked each time a request is created, on the thread creating the request.
        # We can use this to count events, or add callbacks.
        rf.add_callbacks(self.on_success, self.on_error, callback_args=(rf,), errback_args=(rf,))

    def on_success(self, _, response_future):
        # Future callback on a successful request, just record the size.
        self.requests.addValue(response_future.request_encoded_size)

    def on_error(self, _, response_future):
        # Future callback for failed request, record size and increment errors.
        self.requests.addValue(response_future.request_encoded_size)
        self.errors += 1

    def __str__(self):
        # Just extract request count from the size stats (which are recorded on all requests).
        request_sizes = dict(self.requests)
        count = request_sizes.pop('count')
        return "%d requests (%d errors)\nRequest size statistics:\n%s" % (count, self.errors, pp.pformat(request_sizes))


if __name__ == "__main__":
    cluster = Cluster(["127.0.0.1"], port=19042)
    session = cluster.connect()

    ra = RequestAnalyzer(session)
    session.execute("SELECT * FROM people.eployees LIMIT 5;")
    session.execute("SELECT * FROM people.eployees LIMIT 10;")
    session.execute("SELECT * FROM people.eployees LIMIT 15;")
    session.execute("SELECT * FROM people.eployees LIMIT 20;")
    print(ra)
