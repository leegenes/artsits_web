class SpotifyData:
    def __init__(self, oauth):
        self.oauth = oauth
        self.top_artists = []
        self.top_ids = []

    def get_top_artists(self):
        def request_top():
            params = {'limit': 50}
            top50 = self.oauth.request('GET',
                            'v1/me/top/artists',
                            params=params)
            as_json = top50.json()['items']
            return as_json

        def request_related(artist_id):
            related = self.oauth.request('GET',
                    'v1/artists/{id}/related-artists'.format(id=artist_id))
            as_json = related.json()['artists']
            return as_json

        def get_relations(a_id):
            related = request_related(a_id)
            in_top = [r_a['id'] for r_a in related if r_a['id'] in self.top_ids]
            return in_top

        def get_largest_img(images):
            largest = None
            for i in images:
                area = i['height'] * i['width']
                if not largest:
                    largest = {'url': i['url'],
                    'height': i['height'],
                    'width': i['width'],
                    'area': area}
                else:
                    if area > largest['area']:
                        largest['url'] = i['url']
                        largest['height'] = i['height']
                        largest['width'] = i['width']
                        largest['area'] = area
            return largest

        if self.top_artists:
            return self.top_artists
        else:
            top50 = request_top()
            for a in top50:
                self.top_ids.append(a['id'])
                self.top_artists.append({'id': a['id'],
                                'name': a['name'],
                                'popularity': a['popularity'],
                                'img': get_largest_img(a['images']),
                                'related_to': get_relations(a['id']) })
            return self.top_artists
