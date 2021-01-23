<script>
	import { onMount } from 'svelte';
	import CountsCharts from './CountsChart.svelte'
	import EmailCountsCharts from './EmailCountsChart.svelte'
	const API_ROOT = 'http://localhost:2020'
	let spamsCounts = [];
	let emailsCountInMasterDataset = []

	const fetchSpamsCounts = () => {
		fetch(`${API_ROOT}/spams/count`).then((response) => {
			response.json()
			.then((spamsResponse) => {
				spamsCounts = spamsResponse
			})
		}).catch(() => {
			console.error('error')
		})
	}

	const fetchEmailsCounts = () => {
		fetch(`${API_ROOT}/emails/count`).then((response) => {
			response.json()
			.then((countResponse) => {
				emailsCountInMasterDataset = [...emailsCountInMasterDataset, countResponse.count]
			})
		}).catch(() => {
			console.error('error')
		})
	}

	onMount(async () => {
		const spamsCountsIntervalInstance = setInterval(() => {
			fetchSpamsCounts()
		}, 2000)

		const emailsCountsIntervalInstance = setInterval(() => {
			fetchEmailsCounts()
		}, 500)
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
	<div class="d-flex">
		<CountsCharts spamsData={spamsCounts}/>
		<EmailCountsCharts counts={emailsCountInMasterDataset}/>
	</div>
</main>

<footer class="d-flex justify-content-center">
	<ul class="list-group list-group-horizontal">
		<li class="list-group-item">Chopin Johann</li>
		<li class="list-group-item">Duflot Quentin</li>
		<li class="list-group-item">Guidoux Alexandre</li>
		<li class="list-group-item">Weiss Florian</li>
	</ul>
</footer>

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