// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces

declare global {
	namespace App {
		// interface Error {}
		interface Locals {
            db: import('mongodb').Db | null;
        }
		interface PageData {
            shows: import('$lib/types').ShowList;
        }

		// interface PageState {}
		// interface Platform {}
	}
}

export {};
