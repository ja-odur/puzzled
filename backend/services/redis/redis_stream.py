import rx
from .redis import RedisConnection
from ..utils import BaseEncoder, AbstractEncoder


class RedisStream:
    """Class to work with redis stream data"""

    def __init__(self, name_prefix, conn=RedisConnection(), encoder=BaseEncoder()):
        """
        Args:
            name_prefix (str): prefix for redis stream names for easy differentiation
            conn: redis connection
            encoder: class for encoding and decoding (serialization/de-serialization) objects
        """
        if not isinstance(encoder, AbstractEncoder):
            raise Exception(f'{encoder.__class__.__name__} must must inherit from {AbstractEncoder.__name__}')
        self.conn = conn
        self.encoder = encoder
        self.name_prefix = name_prefix

    def add(self, stream_name, fields, id='*', max_len=None, approximate=True):
        """ Method to add fields to a given stream
        Args:
            stream_name (str): the name of the targeted stream
            fields (dict): key/value pairs to insert into the stream
            id (str): Location in the stream to insert this record. By default it is appended
            max_len (int): truncate old stream members beyond this size
            approximate (bool): actual stream length may be slightly more than max_len
        """
        fields = {f'{key}': self.encoder.encode(value) for key, value in fields.items()}
        return self.conn.xadd(
            self.normalized_name(stream_name),
            fields,
            id=id,
            maxlen=max_len,
            approximate=approximate
        )

    def read(self, streams, count=None, block=None):
        """ Method to add fields to a given stream
        Args:
            streams (dict): a dict of stream names to stream IDs, where IDs indicate the last ID already seen.
            count (int): if set, only return this many items, beginning with the earliest available
            block (int): number of milliseconds to wait, if nothing already present
        """
        streams = {f'{self.normalized_name(stream_name)}': id for stream_name, id in streams.items()}
        flat_streams_output = self.conn.xread(streams, count=count, block=block)

        return self._deserialize(flat_streams_output)

    def latest(self, name):
        return self.values(self.range(name, count=1, reverse=True))

    @classmethod
    def values(cls, fields):
        """Extracts actual field dict from the redis field
        Args:
            fields (list): a tuple of redis field objects
        """
        return [field for redis_key, field in fields]

    def range(self, name, start='-', end='+', count=None, reverse=False):
        """Reads stream values within a given interval
        Args:
            name (str): name of the stream
            start (str): first stream ID. defaults to ‘-‘, meaning the earliest available.
            end (str): last stream ID. defaults to ‘+’, meaning the latest available.
            count (int):  if set, only return this many items, beginning with the earliest available.
            reverse (bool): reads stream values within an interval, in reverse order.
        """
        name = self.normalized_name(name)
        if reverse:
            return self._deserialize(
                flat_redis_output=self.conn.xrevrange(name, min=start, max=end, count=count),
                serialize_fields=True
            )
        return self._deserialize(
            flat_redis_output=self.conn.xrange(name, min=start, max=end, count=count),
            serialize_fields=True
        )

    def normalized_name(self, name):
        return f'{self.name_prefix}:{name}'

    def _deserialize(self, flat_redis_output, serialize_fields=False):
        """Method for loading deserialized redis stream outputs

        Args:
            flat_redis_output (list): redis flat outputs
            serialize_fields (bool): flag to indicate whether fields or streams are being serialized
        """
        if serialize_fields:
            return self._deserialize_fields(fields=flat_redis_output)
        return self._deserialize_streams(streams_output=flat_redis_output)

    def _deserialize_streams(self, streams_output):
        """Method for converting redis fields into python objects
        Args:
            streams_output (list): a list of redis stream objects
        """

        # need to deserialize values before returning. there must be a better way!
        return [
            [
                stream_name,
                self._deserialize_fields(fields)
            ]
            for stream_name, fields in streams_output
        ]

    def _deserialize_fields(self, fields):
        """Method for converting redis fields into python objects
        Args:
            fields (list): a tuple of redis field objects
        """
        return [
            (redis_key, {key: self.encoder.decode(value) for key, value in fields.items()})
            for redis_key, fields in fields
        ]

    def poll_stream(self, stream_identifier, parse_stream_data):
        """Function to poll data from redis streams
        Args:
            stream_identifier (str): stream name
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
            .expand(lambda: rx.Observable.from_future(self.read({f'{stream_identifier}': seen_id})))
            .filter(lambda streams: streams)
            .flat_map(lambda streams: streams)
            .flat_map(lambda stream: stream[1])
            .map(lambda stream_event: parse_stream_data(stream_event, stream_identifier))
            .do_action(update_seen_id)
            .finally_action(disconnect)
            .publish()
            .ref_count()
        )
