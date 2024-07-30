<script>
    import FiltersStore from '../stores/FiltersStore.js';

    const setIncluded = () => {
        FiltersStore.update(store => {
            store.included = !store.included;
            return store;
        });
    }
</script>

<div>
    <fieldset>
        <label>
          <input name="included" type="checkbox" role="switch" on:click={setIncluded}/>
          Included only
        </label>
    </fieldset>
</div>