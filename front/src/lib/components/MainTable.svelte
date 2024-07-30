<script>
    import Pagination from "$lib/components/Pagination.svelte";
    import included from '$lib/images/included.png';

    export let data;

    /** @type {import('$lib/types').ShowList} */
    export let shows = data.shows;

    /** @type {import('$lib/types').ShowList} */
    let paginatedDisplayed = [];
    let displayedShows = shows.filter(show => false);
    const displayDuration = (/** @type {number} */ duration) => {
        const hours = Math.floor(duration / 60);
        const minutes = duration % 60;
        return `${hours}h ${minutes}m`;
    }
    const displayedShowsHeaders = ['title', 'included', "rating", 'release_year', 'duration', 'synopsis', 'directors', 'starring'];
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
                    <th scope="row" class="title">{show.title}</th>
                    {#if show.included}
                        <td class="included"><img width="16px" src={included} alt="included" /></td>
                    {:else}
                        <td class="included">{show.price}</td>
                    {/if}
                    <td class="rating">{show.rating == -1.0 ? '?' : show.rating}</td>
                    <td class="release_year">{show.release_year}</td>
                    <td class="duration">{displayDuration(show.duration)}</td>
                    <td class="synopsis">{show.synopsis}</td>
                    <td class="directors">{show.directors}</td>
                    <td class="starring">{show.starring}</td>
                </tr>
            {/each}
        </tbody>
    </table>
    <!-- <SvelteTable columns="{columnSettings}" rows="{paginatedDisplayed}"></SvelteTable> -->
    <Pagination rows={shows} perPage={10} bind:trimmedRows={paginatedDisplayed} />
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
