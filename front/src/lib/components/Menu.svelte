<script>
    import { includedOnly } from '$lib/common/FilterService.js';

    const setIncluded = (/** @type {Event} */ e) => {
        if(e.target != null && e.target instanceof HTMLInputElement) {
            $includedOnly = e.target.checked;
        }
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