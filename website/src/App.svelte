<script>
	import { onMount } from 'svelte';
	import CountsCharts from './CountsCharts.svelte'
	const API_ROOT = 'http://localhost:2020'
	let spamsCounts = [];

	const fetchSpamsCounts = () => {
		fetch(`${API_ROOT}/spams/count`).then((response) => {
			response.json()
			.then((spamsResponse) => {
				spamsCounts = spamsResponse
			})
		}).catch(() => {
			alert('error')
		})
	}

	onMount(async () => {
		const intervalInstance = setInterval(() => {
			fetchSpamsCounts()
		}, 2000)
	})

</script>

<main>
	<h1>λ architecture overview</h1>
	<!--
	<ul id="spams" class="list-group">
		{#each spams as spam}
			<li class="list-group-item">{spam}</li>
		{/each}
	</ul>
	-->
	<CountsCharts spamsData={spamsCounts}/>
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