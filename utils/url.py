from furl import furl


class Url(furl):
    def __init__(self, url=""):
        furl.__init__(self, url)
        self.normalize()

    def normalize(self, scheme="http"):
        # url like 'google.fr' (without 'www') are not correctly parsed
        # by urlparse
        if not self.host:
            self.set(host=str(self.path))
            self.remove(path=True)

        # If there is no scheme, we put http by default
        if not self.scheme:
            self.set(scheme=scheme)

        # We lower case host but not path
        self.set(host=self.host.lower())
        return True

    def __repr__(self):
        return str(self)
