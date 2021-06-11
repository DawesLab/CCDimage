# TODO make this a class that provides a camera object:
import zmq
from numpy import frombuffer

REQUEST_TIMEOUT = 25000
SERVER_ENDPOINT = "tcp://localhost:5555"

def create_client():
    context = zmq.Context()

    #  Socket to talk to server
    print("Connecting to array server...")
    client = context.socket(zmq.REQ)
    client.connect(SERVER_ENDPOINT)

    poll = zmq.Poller()
    poll.register(client, zmq.POLLIN)
    return client, poll

def recv_array(socket, flags=0, copy=False, track=False):
    """recv a numpy array"""
    md = socket.recv_json(flags=flags)
    msg = socket.recv(flags=flags, copy=copy, track=track)
    buf = memoryview(msg)
    A = frombuffer(buf, dtype=md['dtype'])
    return A.reshape(md['shape'])

def request_images(client,N=1):
    shots_requested = N
    request = str(shots_requested)  # ask for one shot of data
    #print "I: Sending (%s)" % request

    client.send(str.encode(request))

def open_images(client,poll):
    socks = dict(poll.poll(REQUEST_TIMEOUT))
    if socks.get(client) == zmq.POLLIN:
        data_array = recv_array(client)
        #reply = client.recv()

        if len(data_array) > 1:  # TODO test for the right size array
            #print "I: Server replied OK: " + str(data_array.shape)
            return data_array

        else:
            # print "E: Malformed reply from server: %s" % reply
            print("E: no reply from server")
            return -1
