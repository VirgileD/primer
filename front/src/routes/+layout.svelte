<script>
	import '@picocss/pico';
	import '../app.css';
</script>

<div class="app">
	<slot />
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
		padding: 1rem;
		margin: 0 auto;
		box-sizing: border-box;
	}
</style>
