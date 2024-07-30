<script>
    /** @type {import('$lib/types').ShowList} */
    export let rows;
    /** @type {number} */
    export let perPage;
    /** @type {import('$lib/types').ShowList} */
    export let trimmedRows;

    /** @type {number} */
    $: totalRows = rows.length;
    /** @type {number} */
    $: totalPages = Math.ceil(totalRows / perPage);
    /** @type {number} */
    $: start = currentPage * perPage;
    /** @type {number} */
    $: end = currentPage === totalPages - 1 ? totalRows - 1 : start + perPage - 1;
    $: trimmedRows = rows.slice(start, end + 1);
    /** @type {number} */
    $: currentPage = currentPage ? (currentPage >= totalPages ? totalPages - 1 : currentPage) : 0;

    /** @typedef { { pagenum: number, class: string } } Page */
    /** @type {Page[]} */
    let pages = [];
    let nbPagesAround = 4;
    $: {
        if (totalPages) {
            // create an array containing its index as value - these are the page num (0-indexed)
            pages = [...new Array(totalPages)].map(function (_, i) {
                return { pagenum: i + 1, class: i == currentPage ? 'current' : 'normal' };
            });
            // only keep the curr page and its neighbors.
            if (totalPages > currentPage + nbPagesAround) {
                pages = pages.slice(0, currentPage + nbPagesAround);
            }
            if (currentPage > nbPagesAround) {
                pages = pages.slice(currentPage - nbPagesAround);
            }
            if (totalPages > nbPagesAround * 2) {
                while (pages.length < nbPagesAround * 2) {
                    // we can add some pages.
                    if (pages[0].pagenum > 1) {
                        pages.unshift({ pagenum: pages[0].pagenum - 1, class: 'normal' });
                    }
                    if (pages[pages.length - 1].pagenum < totalPages) {
                        pages.push({ pagenum: pages[pages.length - 1].pagenum + 1, class: 'normal' });
                    }
                }
            }
            if (pages[0].pagenum > 1) {
                if (pages[pages.length - 1].pagenum < totalPages - 1) {
                    pages.unshift({ pagenum: 0, class: 'three-dot' });
                    pages.push({ pagenum: 0, class: 'three-dot' });
                } else {
                    if (pages[0].pagenum > 2) {
                        pages.unshift({ pagenum: pages[0].pagenum - 1, class: 'normal' });
                        pages.unshift({ pagenum: 0, class: 'three-dot' });
                    } else {
                        // not much we can do, we're odd
                    }
                }
            } else {
                if (pages[pages.length - 1].pagenum < totalPages - 1) {
                    if (pages[pages.length - 1].pagenum < totalPages - 2) {
                        pages.push({ pagenum: pages[pages.length - 1].pagenum + 1, class: 'normal' });
                    } else {
                        // we're odd here too
                    }
                    pages.push({ pagenum: 0, class: 'three-dot' });
                }
            }
        }
    }
</script>

{#if totalRows && totalRows > perPage}
    <div class="container">
        <div role="group">
                <button  class="outline secodary" on:click={() => (currentPage = 0)} disabled={currentPage === 0 ? true : false}>
                    &lt;&lt;
                </button>
                <button  class="outline primary" on:click={() => (currentPage -= 1)} disabled={currentPage === 0 ? true : false}>
                    &lt;
                </button>
                {#each pages as page}
                        <button
                            class="{page.class}"
                            on:click={() => {
                                if (page.class == 'normal') currentPage = page.pagenum - 1;
                            }}
                        >
                            {page.pagenum == 0 ? "..." : page.pagenum}
                        </button>
                {/each}
                <button class="outline primary" on:click={() => (currentPage += 1)} disabled={currentPage === totalPages - 1 ? true : false}>
                    &gt;
                </button>
                <button class="outline secondary" on:click={() => (currentPage = totalPages - 1)} disabled={currentPage === totalPages - 1 ? true : false}>
                    &gt;&gt;
                </button>
        </div>
    </div>
    <div class="container">
        <div>
            <div>
                {totalPages} pages of {perPage} short urls
            </div>
        </div>
    </div>
{/if}

<style lang="scss">
   button {
        display: flex;
        margin: 0.5em;
        padding: 0.1em;
        justify-content: center;
        width: 5ch;
        max-width: 5ch;
        display: inline-block;
    }
    .current {
        background-color: transparent;
        color: var(--pico-primary);
        border: 1px solid var(--primary);
        cursor: default;
    }
    .normal {
        background-color: transparent;
        color: var(--pico-secondary);
        border: 1px solid var(--pico-secondary);
    }
</style>
