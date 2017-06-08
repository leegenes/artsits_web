class SpotifyData:
    def __init__(self, oauth):
        self.oauth = oauth
        self.top_artists = []
        self.relations = []

    def get_top_artists(self):
        def request_top():
            params = {'limit': 50}
            top50 = self.oauth.request('GET',
                            'v1/me/top/artists',
                            params=params)
            as_json = top50.json()['items']
            return as_json

        def get_smallest_img(images):
            smallest = None
            for i in images:
                area = i['height'] * i['width']
                if not smallest:
                    smallest = (i['url'], area)
                else:
                    if area < smallest[1]:
                        smallest = (i['url'], area)
            return smallest[0]

        if self.top_artists:
            return self.top_artists
        else:
            top50 = request_top()
            for a in top50:
                self.top_artists.append({'id': a['id'],
                                'name': a['name'],
                                'popularity': a['popularity'],
                                'img': get_smallest_img(a['images']),
                                'id': a['id']})
            return self.top_artists

    def get_relations(self):
        def request_related(artist_id):
            related = self.oauth.request('GET',
                    'v1/artists/{id}/related-artists'.format(id=artist_id))
            as_json = related.json()['artists']
            return as_json

        for a in self.top_artists:
            related = request_related(a['id'])
            in_top = [r_a['id'] for r_a in related if r_a['id'] in self.top_artists]
            self.relations.append({a['id']: in_top})
        return self.relations
