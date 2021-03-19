<script>
	import { onMount } from 'svelte';
	import Description from './Description.svelte'
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
	<div class="d-flex charts">
		<SenderSpammerCountsChart spamsData={spamsCounts}/>
		<EmailCountsCharts counts={emailsCountInMasterDataset}/>
		<SpamsAmountSpeedVsBatchChart data={spamsEmailSpeedBatch} />
	</div>

	<Description />
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

	.charts {
		width: 100%;
		overflow: scroll;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>