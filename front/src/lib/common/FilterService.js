import { writable } from 'svelte/store';

let includedOnly = writable(false);
let genresFilter = writable([]);
let moodsFilter = writable([]);
let ratingMin = writable(0);
let ratingMax = writable(10);
let yearMin = writable(1900);
let yearMax = writable(2022);
let wordsFilter = writable([]);

export {
        includedOnly,
        genresFilter,
        moodsFilter,
        ratingMin,
        ratingMax,
        yearMin,
        yearMax,
        wordsFilter
};