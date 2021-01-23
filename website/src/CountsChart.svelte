<script>
  import FusionCharts from 'fusioncharts';
  import Charts from 'fusioncharts/fusioncharts.charts';
  import FusionTheme from 'fusioncharts/themes/fusioncharts.theme.fusion';
  import SvelteFC, { fcRoot } from 'svelte-fusioncharts';

  export let spamsData

  const getChartData = (data) => {
    const sortedTimestamps = data.map(a => parseInt(a.timestamp)).sort()
    let chartData = []

    sortedTimestamps.forEach(timestamp => {
      chartData.push([timestamp, data.find(elmt => elmt.timestamp === timestamp.toString()).count])
    });

    return chartData.map((spam) => {
      return {
        label: spam[0],
        value: spam[1]
      }
    })
  }

  // Always set FusionCharts as the first parameter
  fcRoot(FusionCharts, Charts, FusionTheme);

  $: dataSource = {
    chart: {
      caption: 'Detected spams emails from batch process',
      xAxisName: 'Timestamp',
      yAxisName: 'Detected spams',
      theme: 'fusion'
    },
    data: getChartData(spamsData)
  };

  $: chartConfigs = {
    type: 'line',
    width: 600,
    height: 400,
    dataFormat: 'json',
    dataSource: dataSource
  };
</script>

<SvelteFC {...chartConfigs} />