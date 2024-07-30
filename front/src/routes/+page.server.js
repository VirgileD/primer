
/** @type {import('./$types').PageServerLoad} */
export async function load(event) {
    if (event.locals.db === undefined) {
        throw new Error('db is undefined');
    }
    /** @type {import('mongodb').Collection<import('$lib/types').Show>} */
    // @ts-ignore event.locals.db cannot be null at this point
    const enriched = event.locals.db.collection('enriched')
    /** @type {import('$lib/types').ShowList} */
    let shows = await enriched.find({ $or: [ { rating: { $gte: 3.5 }}, { rating: -1.0 } ] }).toArray();
    shows = shows.map(show => { return { ...show, _id: show._id.toString() } })
    // default sort by rating, then release year, then title
    shows.sort((a, b) => {
        if (a.rating > b.rating) {
            return -1;
        }
        if (a.rating < b.rating) {
            return 1;
        }
        if (a.release_year > b.release_year) {
            return -1;
        }
        if (a.release_year < b.release_year) {
            return 1;
        }
        if (a.title > b.title) {
            return -1;
        }
        if (a.title < b.title) {
            return 1;
        }
        return 0;
    });
    /** @type {string[]} */
    let genres = await enriched.distinct("genres", { $or: [ { rating: { $gte: 3.5 }}, { rating: -1.0 } ] })
    /** @type {string[]} */
    let moods = await enriched.distinct("moods", { $or: [ { rating: { $gte: 3.5 }}, { rating: -1.0 } ] })
    //console.log(shows);

    return {
        shows,
        genres,
        moods
    }
}