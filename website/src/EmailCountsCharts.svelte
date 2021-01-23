<script>
  import FusionCharts from 'fusioncharts';
  import Charts from 'fusioncharts/fusioncharts.charts';
  import FusionTheme from 'fusioncharts/themes/fusioncharts.theme.fusion';
  import SvelteFC, { fcRoot } from 'svelte-fusioncharts';

  export let counts

  const getChartData = (data) => {
    return data.map((count) => {
      return {
        value: count
      }
    })
  }

  // Always set FusionCharts as the first parameter
  fcRoot(FusionCharts, Charts, FusionTheme);

  $: dataSource = {
    chart: {
      caption: 'Amount of emails stored in Master dataset',
      yAxisName: 'Amount of emails',
      theme: 'fusion'
    },
    data: getChartData(counts)
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