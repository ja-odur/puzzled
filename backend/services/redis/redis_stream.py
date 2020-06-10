from pickle import loads, dumps
import rx
from .redis import RedisConnection


class RedisStream:
    """Class to work with redis stream data"""

    def __init__(self, name_prefix, conn=RedisConnection()):
        """
        Args:
            name_prefix (str): prefix for redis stream names for easy differentiation
            conn: redis connection
        """
        self.conn = conn
        self.name_prefix = name_prefix

    def add(self, stream_name, fields, id='*', max_len=None, approximate=True, serializer=dumps):
        """ Method to add fields to a given stream
        Args:
            stream_name (str): the name of the targeted stream
            fields (dict): key/value pairs to insert into the stream
            id (str): Location in the stream to insert this record. By default it is appended
            max_len (int): truncate old stream members beyond this size
            approximate (bool): actual stream length may be slightly more than max_len
            serializer (func): function to serialise complex python objects before dumping to redis. pickle is default
        """
        fields = {f'{key}': serializer(value) for key, value in fields.items()}
        return self.conn.xadd(
            self.normalized_name(stream_name),
            fields,
            id=id,
            maxlen=max_len,
            approximate=approximate
        )

    def read(self, streams, count=None, block=None, deserializer=loads):
        """ Method to add fields to a given stream
        Args:
            streams (dict): a dict of stream names to stream IDs, where IDs indicate the last ID already seen.
            count (int): if set, only return this many items, beginning with the earliest available
            block (int): number of milliseconds to wait, if nothing already present
            deserializer (func): function to deserialize redis objects into python objects
        """
        streams = {f'{self.normalized_name(stream_name)}': id for stream_name, id in streams.items()}
        flat_streams_output = self.conn.xread(streams, count=count, block=block)

        # need to deserialize values before returning. there must be a better way!
        return [
            [
                stream_name,
                [
                    (redis_key, {key: deserializer(value) for key, value in fields.items()})
                    for redis_key, fields in fields
                ]
            ]
            for stream_name, fields in flat_streams_output
        ]

    def normalized_name(self, name):
        return f'{self.name_prefix}:{name}'

    def poll_stream(self, stream_name, parse_stream_data):
        """Function to poll data from redis streams
        Args:
            stream_name (str): stream name
            parse_stream_data: method for serializing final message
        """
        seen_id = None

        def update_seen_id(stream_event):
            nonlocal seen_id
            if seen_id is None or stream_event.id > seen_id:
                seen_id = stream_event.id

        def disconnect():
            self.conn.quit()

        return (
            rx.Observable.of(None)
            .expand(lambda: rx.Observable.from_future(self.read({f'{stream_name}': seen_id})))
            .filter(lambda streams: streams)
            .flat_map(lambda streams: streams)
            .flat_map(lambda stream: stream[1])
            .map(lambda stream_event: parse_stream_data(stream_event, stream_name))
            .do_action(update_seen_id)
            .finally_action(disconnect)
            .publish()
            .ref_count()
        )
