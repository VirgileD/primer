export type Show = {
    _id: string|import('mongodb').ObjectId;
    id: string;
    title: string;
    type: 'Movie'|'TV Show'|'Rent';
    url: string;
    synopsis: string;
    rating: number;
    categories: string[];
    genres: string[];
    moods: string[];
    duration: number;
    release_year: number;
    directors: string[];
    starring: string[];
    price: number;
    included: boolean;
    duration: number;
};

export type ShowList = Show[];

export type FilterFunction = (s : Show) => boolean;

export type Filters = {
    type: keyof Show;
    filter: FilterFunction;
};