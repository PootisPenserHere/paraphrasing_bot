import urllib.parse
import requests


class String:
    @staticmethod
    def url_builder(*args) -> str:
        encoded_url = urllib.parse.urljoin(args[0], "/".join(urllib.parse.quote_plus(part.strip("/"), safe="/") for part in args[1:]))
        decoded = requests.utils.unquote(encoded_url)

        if '/?' in decoded:
            return decoded.replace('/?', '?')
        else:
            return decoded
