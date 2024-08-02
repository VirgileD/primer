import { init } from '$lib/common/db.server';
import { building } from '$app/environment';

/** @type {import('mongodb').Db | null} */
let dbConn = null;

/**
 * Initializes the database connection by running all the necessary initialization functions.
 * @returns {Promise<void>}
 */
const runAllTheInitFunctions = async () => {
	dbConn = await init();
};
if (!building) {
	await runAllTheInitFunctions();
}

/** @type {import('@sveltejs/kit').Handle} */
export const handle = async ({ event, resolve }) => {
	if (dbConn === null) {
		await runAllTheInitFunctions();
	}
	event.locals.db = dbConn;
	return resolve(event);
};
