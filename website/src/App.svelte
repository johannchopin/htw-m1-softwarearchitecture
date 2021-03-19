<script>
	import { onMount } from 'svelte';
	import SenderSpammerCountsChart from './SenderSpammerCountsChart.svelte'
	import EmailCountsCharts from './EmailCountsChart.svelte'
	import SpamsAmountSpeedVsBatchChart from './SpamsAmountSpeedVsBatchChart.svelte'
	const API_ROOT = 'http://localhost:2020'
	let spamsCounts = [];
	let emailsCountInMasterDataset = []
	let spamsEmailSpeedBatch = []

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

	const fetchSpeedBatchSpamsDetectionCounts = () => {
		fetch(`${API_ROOT}/difference/batch-speed/spams/count`).then((response) => {
			response.json()
			.then((countResponse) => {
				const now = new Date().getTime()
				const data = {
					timestamp: now,
					batch: countResponse.batch,
					speed: countResponse.speed
				}
				spamsEmailSpeedBatch = [...spamsEmailSpeedBatch, data]
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

		const speedBatchSpamsDetectionCountsIntervalInstance = setInterval(() => {
			fetchSpeedBatchSpamsDetectionCounts()
		}, 1000)
	})
</script>

<main>
	<h1>λ architecture overview</h1>
	<div class="d-flex">
		<SenderSpammerCountsChart spamsData={spamsCounts}/>
		<EmailCountsCharts counts={emailsCountInMasterDataset}/>
		<SpamsAmountSpeedVsBatchChart data={spamsEmailSpeedBatch} />
	</div>
</main>

<footer class="d-flex justify-content-center">
	<ul class="list-group list-group-horizontal">
		<li class="list-group-item">Johann Chopin</li>
		<li class="list-group-item">Quentin Duflot</li>
		<li class="list-group-item">Alexandre Guidoux</li>
		<li class="list-group-item"><a href="https://fweiss.com">Florian Weiss</a></li>
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