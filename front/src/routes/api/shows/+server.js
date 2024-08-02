import { error, json } from '@sveltejs/kit';

/** @type {import('@sveltejs/kit').RequestHandler} */
export async function GET(event) {
    let skip = parseInt(event.url.searchParams.get('idx') || '0', 10);
    try {
        if (event.locals.db === undefined) {
            throw new Error('db is undefined');
        }
        /** @type {import('mongodb').Collection<import('$lib/types').Show>} */
        // @ts-ignore event.locals.db cannot be null at this point
        const enriched = event.locals.db.collection('enriched');
        /** @type {import('$lib/types').ShowList} */
        let shows = await enriched.find({ $or: [{ rating: { $gte: 3.5 } }, { rating: -1.0 }] }).skip(skip).limit(250).sort({ rating: -1, release_year:-1, title: 1 }).toArray();
    
		return json( shows, { status: 200 });
	} catch (err) {
		console.error(`Error while fetching shows from ${skip}: ${err}`)
        if(err instanceof Error) {
            error(500, err );
        } else {
            error(500, { message: "Unknow error" } );
        }
        
	}
}