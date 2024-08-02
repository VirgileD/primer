import unittest
import enrich_helpers.enrich as enrich

class TestEnrich(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        self.maxDiff = None
        super().__init__(methodName)

    def test_included_movie(self):
        with open('test_assets/movie-included.html', 'r') as f:
            html_string = f.read()
        included_movie = enrich.enrich_show({ "type": "Movie", "categories": [] }, html_string)
        #print(included_movie)
        self.assertEqual(included_movie, {'type': 'Movie', 'categories': ['N/A'], 'rating': 6.4, 'duration': 105, 'release_year': 2024, 'genres': ['Action', 'Suspense', 'Drama'], 'moods': ['N/A'], 'starring': ['Jason Statham', 'Emmy Raver-Lampman', 'Bobby Naderi'], 'directors': ['David Ayer'], 'synopsis': 'In "The Beekeeper," one man’s brutal campaign for vengeance takes on national stakes after he is revealed to be a former operative of a powerful and clandestine organization known as “Beekeepers.” Jason Statham stars in this action-packed thriller.', 'included': True, 'price': 0})

    def test_included_tvshow(self):
        with open('test_assets/tvshow-included.html', 'r') as f:
            html_string = f.read()
        included_tvshow = enrich.enrich_show({ "type": "TV Show", "categories": [] }, html_string)
        #print(included_tvshow)
        self.assertEqual(included_tvshow, {'type': 'TV Show', 'categories': ['N/A'], 'rating': 8.7, 'duration': 62, 'release_year': 2024, 'genres': ['Action', 'Science Fiction', 'Drama', 'Comedy'], 'moods': ['N/A'], 'starring': ['Karl Urban', 'Jack Quaid', 'Antony Starr'], 'directors': ['Philip Sgriccia', 'Frederick E.O. Toye', 'Sarah Boyd', 'Eric Kripke', 'Stefan Schwartz', 'Nelson Cragg', 'Julian Holmes', 'Karen Gaviola', 'Daniel Attias', 'Jennifer Phang'], 'synopsis': 'The world is on the brink. Victoria Neuman is closer than ever to the Oval Office and under Homelander’s muscly thumb as he consolidates his power. Butcher, with only months to live, has lost Becca’s son, and his job as The Boys’ leader. The rest of the team are fed up with his lies. With the stakes higher than ever, they must find a way to work together and save the world before it’s too late.', 'included': True, 'seasons': 4, 'episodes': 8, 'price': 0})

    def test_rent_movie(self):
        with open('test_assets/movie-rent.html', 'r') as f:
            html_string = f.read()
        rent_movie = enrich.enrich_show({ "type": "Movie", "categories": [] }, html_string)
        #print(rent_movie)
        self.assertEqual(rent_movie, {'type': 'Movie', 'categories': ['N/A'], 'rating': 8.6, 'duration': 165, 'release_year': 2024, 'genres': ['Action', 'Adventure', 'Drama', 'Science Fiction'], 'moods': ['N/A'], 'starring': ['Timothée Chalamet', 'Zendaya', 'Rebecca Ferguson'], 'directors': ['Denis Villeneuve'], 'synopsis': 'Dune: Part Two explores the mythic journey of Paul Atreides as he unites with Chani and the Fremen while on a warpath of revenge against the conspirators who destroyed his family. Facing a choice between the love of his life and the fate of the known universe, he endeavors to prevent a terrible future only he can foresee.', 'included': False, 'price': 4.99})

    def test_index_range(self):
        with open('test_assets/index_range.html', 'r') as f:
            html_string = f.read()
        index_range = enrich.enrich_show({ "type": "Movie", "categories": [] }, html_string)
        #print(index_range)
        self.assertEqual(index_range, {'type': 'Movie', 'genres': ['Action', 'Adventure'], 'moods': ['Exciting', 'Tense'], 'categories': ['N/A'], 'rating': 6.5, 'duration': 108, 'release_year': 1996, 'starring': ['Helen Hunt', 'Bill Paxton', 'Jami Gertz'], 'directors': ['Jan De Bont'], 'synopsis': "Storm-chasing scientists head into the heart of the most lethal tornadoes to track nature's fury in this action-packed blockbuster with Helen Hunt and Bill Paxton.", 'price': 3.99, 'included': False})

    def test_genres(self):
        with open('test_assets/genres.html', 'r') as f:
            html_string = f.read()
        multi_genres = enrich.enrich_show({ "type": "Movie", "categories": [] }, html_string)
        #print(multi_genres)
        self.assertEqual(multi_genres, {'type': 'Movie', 'categories': [], 'rating': 6.9, 'duration': 106, 'release_year': 2002, 'genres': ['Erotic', 'Drama'], 'moods': ['Quirky', 'Strange'], 'starring': ['James Spader', 'Maggie Gyllenhaal', 'Jeremy Davies'], 'directors': ['Steven Shainberg'], 'synopsis': 'After checking out of a mental institution, a woman works for an attorney who shares her enthusiasm for sadomasochism.', 'included': False, 'price': 3.99})

if __name__ == '__main__':
    unittest.main()