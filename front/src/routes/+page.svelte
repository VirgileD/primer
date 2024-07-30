<script>
    import MainTable from '../lib/components/MainTable.svelte';
    import Menu from '../lib/components/Menu.svelte';

    /** @type {import('./$types').PageData} */
    export let data;
</script>

<svelte:head>
	<title>My Primer Prime</title>
	<meta name="description" content="My Primer Prime demo app" />
</svelte:head>

<container>
    <div>
        <Menu />
    </div>
    <div>
        <MainTable {data} />
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
