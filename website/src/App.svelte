<script>
	import { onMount } from 'svelte';
	const API_ROOT = 'http://localhost:2020'
	let spams = [];

	const fetchSpams = () => {
		fetch(`${API_ROOT}/spams`).then((response) => {
			console.log(response.body)
		}).catch(() => {
			spams = ["test@test.com", "test2@test.com"]
		})
	}

	onMount(async () => {
		fetchSpams()
		const intervalInstance = setInterval(() => {
			fetchSpams()
		}, 5000)
	})

</script>

<main>
	Hi penis
	<ul id="spams" class="list-group">
		{#each spams as spam}
			<li class="list-group-item">{spam}</li>
		{/each}
	</ul>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>