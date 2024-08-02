<script>
	import Pagination from '$lib/components/Pagination.svelte';
	import included from '$lib/images/included.png';
	import link from '$lib/images/link.png';
	import {
		includedOnly,
		genresFilter,
		wordsFilter,
		ratingMin
	} from '$lib/common/FilterService.js';

	export let data;

	/** @type {import('$lib/types').ShowList} */
	export let shows = data.shows;

	/** @type {import('$lib/types').ShowList} */
	let paginatedDisplayed = [];

	$: displayedShows = shows.filter((show) => {
		let filter = true;
		if ($includedOnly) {
			filter = filter && show.included;
		}
		if ($genresFilter.length > 0) {
			filter = filter && $genresFilter.every((/** @type {string} */ genre) => show.genres.includes(genre));
		}

		if ($wordsFilter.length > 0) {
			let appears = $wordsFilter.some(
				(/** @type {string} */w) => show.title.toLowerCase().includes(w.toLowerCase())
			);
			appears =
				appears ||
				$wordsFilter.some(
					(/** @type {string} */w)  => show.synopsis.toLowerCase().includes(w.toLowerCase())
				);
			appears =
				appears ||
				$wordsFilter.some(
					(/** @type {string} */w)  =>
						show.starring.join(',').toLowerCase().includes(w.toLowerCase())
				);
			filter = filter && appears;
		}
		return filter && show.rating >= $ratingMin;
	});

	const displayedShowsHeaders = [
		'title',
		'included',
		'rating',
		'synopsis',
		'genres',
		'release_year'
	];
</script>

<section>
	<table class="striped">
		<thead>
			<tr>
				{#each displayedShowsHeaders as header}
					<th scope="col" class="header header-{header}">{header.replace('_', ' ')}</th>
				{/each}
			</tr>
		</thead>
		<tbody>
			{#each paginatedDisplayed as show}
				<tr>
					<th scope="row" class="title"
						>{show.title}&nbsp;<a href={show.url} target="_blank"
							><img src={link} width="16px" alt="link to details" /></a
						></th
					>
					{#if show.included}
						<td class="included"><img width="16px" src={included} alt="included" /></td>
					{:else}
						<td class="included">€ {show.price}</td>
					{/if}
					<td class="rating">{show.rating == -1.0 ? '?' : show.rating}</td>
					<td class="synopsis">{show.synopsis}</td>
					<td class="genres">{show.genres.join(', ')}</td>
					<td class="release_year">{show.release_year}</td>
				</tr>
			{/each}
		</tbody>
	</table>
	<!-- <SvelteTable columns="{columnSettings}" rows="{paginatedDisplayed}"></SvelteTable> -->
	<Pagination rows={displayedShows} perPage={10} bind:trimmedRows={paginatedDisplayed} />
</section>

<style>
	table {
		margin-left: 2em;
		margin-top: 2em;
	}
	.header {
		text-transform: capitalize;
		font-weight: bold;
	}
	.title {
		font-size: large;
		font-weight: bold;
	}
	.synopsis {
		max-width: 400px;
		width: 400px;
		font-size: small;
	}
</style>
