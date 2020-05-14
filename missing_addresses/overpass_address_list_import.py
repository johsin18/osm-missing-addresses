from io import StringIO
from urllib.request import urlopen
from urllib.error import HTTPError
import re
from overpy import exception
from typing import List, Tuple

from missing_addresses import CsvAddressListImport, Address, OsmPrimitive


class OverpassAddressListImport:
    """
    Class to access the Overpass API
    """
    default_read_chunk_size = 4096
    default_url = "http://overpass-api.de/api/interpreter"

    def __init__(self, read_chunk_size=None, url=None):
        """
        :param read_chunk_size: Max size of each chunk read from the server response
        :type read_chunk_size: Integer
        :param url: Optional URL of the Overpass server. Defaults to http://overpass-api.de/api/interpreter
        :type url: str
        """
        self.url = self.default_url
        if url is not None:
            self.url = url

        self._regex_extract_error_msg = re.compile(b"\<p\>(?P<msg>\<strong\s.*?)\</p\>")
        self._regex_remove_tag = re.compile(b"<[^>]*?>")
        if read_chunk_size is None:
            read_chunk_size = self.default_read_chunk_size
        self.read_chunk_size = read_chunk_size

    def query(self, query) -> str:
        """
        Query the Overpass API

        :param String|Bytes query: The query string in Overpass QL
        :return: The parsed result
        :rtype: overpy.Result
        """
        if not isinstance(query, bytes):
            query = query.encode("utf-8")

        try:
            f = urlopen(self.url, query)
        except HTTPError as e:
            f = e

        response = f.read(self.read_chunk_size)
        while True:
            data = f.read(self.read_chunk_size)
            if len(data) == 0:
                break
            response = response + data
        f.close()

        if f.code == 200:
            content_type = f.getheader("Content-Type")

            if content_type != "text/csv":
                raise exception.OverpassUnknownContentType(content_type)

            if isinstance(response, bytes):
                response = response.decode("utf-8")

            return response

        if f.code == 400:
            msgs = []
            for msg in self._regex_extract_error_msg.finditer(response):
                tmp = self._regex_remove_tag.sub(b"", msg.group("msg"))
                try:
                    tmp = tmp.decode("utf-8")
                except UnicodeDecodeError:
                    tmp = repr(tmp)
                msgs.append(tmp)

            raise exception.OverpassBadRequest(
                query,
                msgs=msgs
            )

        if f.code == 429:
            raise exception.OverpassTooManyRequests

        if f.code == 504:
            raise exception.OverpassGatewayTimeout

        raise exception.OverpassUnknownHTTPStatusCode(f.code)

    def read(self, area_id, print_query=True) -> List[Tuple[Address, OsmPrimitive]]:
        print("Querying Overpass...")
        query_string: str = f"""
[out:csv("addr:street","addr:place","addr:housenumber",::type,::id;true;",")];
nwr({area_id});
map_to_area -> .queryarea;
(nwr(area.queryarea)["addr:street"]["addr:housenumber"]; nwr(area.queryarea)["addr:place"]["addr:housenumber"];);
out;
"""
        if print_query:
            print(query_string)

        csv_content = self.query(query_string)

        return CsvAddressListImport.read_actual(StringIO(csv_content))
