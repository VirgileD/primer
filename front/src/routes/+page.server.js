/** @type {import('./$types').PageServerLoad} */
export async function load(event) {
	if (event.locals.db === undefined) {
		throw new Error('db is undefined');
	}
	/** @type {import('mongodb').Collection<import('$lib/types').Show>} */
	// @ts-ignore event.locals.db cannot be null at this point
	const enriched = event.locals.db.collection('enriched');
	/** @type {import('$lib/types').ShowList} */
	let shows = await enriched.find({ $or: [{ rating: { $gte: 3.5 } }, { rating: -1.0 }] }).limit(250).sort({ rating: -1, release_year:-1, title: 1 }).toArray();
	shows = shows.map((show) => {
		return { ...show, _id: show._id.toString() };
	});
	/** @type {string[]} */
	let genres = await enriched.distinct('genres', {
		$or: [{ rating: { $gte: 3.5 } }, { rating: -1.0 }]
	});
    let totalShows = await enriched.countDocuments({ $or: [{ rating: { $gte: 3.5 } }, { rating: -1.0 }] });
	
	return {
		shows,
		genres,
        totalShows
	};
}
