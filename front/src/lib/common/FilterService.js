import { writable } from 'svelte/store';

function createFiltersStore = () => {
    
    let includedOnly = true;
    const setIncludedOnly = (value) => {
        includedOnly = value;
    }
    
    let genres = [];
    const setGenres = (value) => {
        genres = value;
    }

    let ratingMin = 0;
    let ratingMax = 10;
    const setRating = (min, max) => {
        ratingMin = min;
        ratingMax = max;
    }

    let yearMin = 1900;
    let yearMax = 2021;
    const setYear = (min, max) => {
        yearMin = min;
        yearMax = max;
    }

    let wordsFilter = []
    const setWordsFilter = (value) => {
        wordsFilter = value;
    }

    const filter = (/** @type {import('$lib/types').ShowList} */ shows) => {
        let filtered = shows.filter(show => {
            if (includedOnly && !show.included) return false;
            if (genres.length > 0 && !genres.includes(show.genres)) return false;
            if (show.rating < ratingMin || show.rating > ratingMax) return false;
            if (show.year < yearMin || show.year > yearMax) return false;
            if (wordsFilter.length > 0) {
                for (let word of wordsFilter) {
                    if (!show.title.includes(word) && !show.synopsis.includes(word) && !show.starring.join(',').includes(word)) {
                        return false;
                    }
                }
            }
            return true;
        }
        )

    }
}

export const FilterService = createFiltersStore()