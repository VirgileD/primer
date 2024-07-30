<script>
    import { includedOnly, genresFilter, moodsFilter, ratingMin,wordsFilter } from '$lib/common/FilterService.js';
	import { onMount } from 'svelte';

    export let data;
    const genres = data.genres;

    const setIncluded = (/** @type {Event} */ e) => {
        if(e.target != null && e.target instanceof HTMLInputElement) {
            $includedOnly = e.target.checked;
        }
    }
    const setGenre = ( /** @type { { target: HTMLInputElement } } */  { target }) => {
        if(target!=null) {
            if(target.checked) {
                $genresFilter = Array.from(new Set([...$genresFilter, target.name]))
            } else {
                $genresFilter = $genresFilter.filter(genre => genre !== target.name);
            }
        }
        console.log($genresFilter);
    }

    const setWordsFilter = (/** @type {Event} */ e) => {
        if(e.target != null && e.target instanceof HTMLInputElement) {
            $wordsFilter = e.target.value.split(' ');
        }
        console.log($wordsFilter)
    }

    onMount(() => {
        $wordsFilter = [];
        $ratingMin = 3.5;
    });
</script>

<div>
    <section>
        <fieldset>
            <label>
            <input name="included" type="checkbox" role="switch" on:click={setIncluded}/>
            Included only
            </label>
        </fieldset>
    </section>
    <section>
        <fieldset>
            <legend>Search words</legend>
            <input name="words" type="text" on:click={setWordsFilter} />
        </fieldset>
    </section>
    <section>
        <fieldset>
            <legend>Min Rating</legend>
            <input name="minrating" type="number" bind:value={$ratingMin} min="3.5" max="10" step="0.1"/>
        </fieldset>
    </section>
    <section>
        <fieldset>
            <legend>Genres</legend>
            <ul class="kinda">
                {#each genres as genre}
                    <li><input name="{genre}" type="checkbox" on:click={setGenre}/>{genre}</li>
                {/each}
            </ul>
        </fieldset>
    </section>
</div>

<style>
    fieldset {
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 0.5rem;
        overflow-y: hidden;
    }
    .kinda {
        list-style: none;
        padding: 0;
        margin: 0;
        font-size: smaller;
        white-space: nowrap;
    }
    
</style>