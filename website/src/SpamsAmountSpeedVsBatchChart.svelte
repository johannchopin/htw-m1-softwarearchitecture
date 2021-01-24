<script>
  import FusionCharts from 'fusioncharts';
  import Charts from 'fusioncharts/fusioncharts.charts';
  import FusionTheme from 'fusioncharts/themes/fusioncharts.theme.fusion';
  import SvelteFC, { fcRoot } from 'svelte-fusioncharts';

  // type [{timestamp: number, batch: number, speed: numbre}, ...] 
  export let data

  const getChartData = (data) => {
    let speedData = {
      seriesname: "Speed layer",
      data: []
    }
    let batchData = {
      seriesname: "Batch layer",
      data: []
    }
  
    data.forEach(countsObject => {
      speedData.data.push({value: countsObject.speed})
      batchData.data.push({value: countsObject.batch})
    })

    return [speedData, batchData]
  }

  const getCategories = (data) => {
    return data.map(countsObject => {
      return {
        label: countsObject.timestamp
      }
    })
  }

  // Always set FusionCharts as the first parameter
  fcRoot(FusionCharts, Charts, FusionTheme);

  $: dataSource = {
    chart: {
      caption: 'Amount of emails detected as a spam',
      yAxisName: 'Amount of emails',
      theme: 'fusion'
    },
    categories: [
      {
        category: getCategories(data)
      }
    ],
    dataset: getChartData(data)
  };

  $: chartConfigs = {
    type: 'msline',
    width: 600,
    height: 400,
    dataFormat: 'json',
    dataSource: dataSource
  };
</script>

<SvelteFC {...chartConfigs} />