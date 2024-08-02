<script>
	import { onMount } from 'svelte';
	import MainTable from '../lib/components/MainTable.svelte';
	import Menu from '../lib/components/Menu.svelte';

	/** @type {import('./$types').PageData} */
	export let data;
    $: loading = true;
    /** @type {import('$lib/types').ShowList} */
    $: shows = data.shows;
    
    const loadMore = async () => {
        const res = await fetch('http://localhost:5173/api/shows?idx=' + shows.length);
        shows.push(...await res.json());
        shows = [...shows];
        console.log('loading more: '+shows.length);
        if(shows.length < data.totalShows) {
            setTimeout(loadMore, 1000);
        } else {
            loading = false;
        }
    }
    onMount(async () => {
        loadMore();
    });
</script>

<svelte:head>
	<title>My Primer Prime</title>
	<meta name="description" content="My Primer Prime demo app" />
</svelte:head>

<container>
	<div>
		<Menu {data} />
	</div>
	<div>
		<MainTable {shows} {loading} />
	</div>
</container>

<style>
	container {
		display: grid;
		grid-template-columns: 0.2fr 1.8fr;
		grid-column-gap: 20px;
		justify-items: stretch;
		align-items: stretch;
	}
</style>
