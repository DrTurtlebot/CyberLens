<template>
  <div>
    <b class="text-2xl 4k:text-5xl">Abuse IP</b>

    <!-- Loading Spinner -->
    <div v-if="loading" class="flex items-center justify-center space-x-2">
      <span>Loading</span>
      <svg class="animate-spin h-5 w-5 text-black dark:text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.963 7.963 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>

    <p v-if="error">Error: {{ error }}</p>

    <div v-if="responseData">
      <div v-if="responseData.Error">
        <p>Error: {{ responseData.Error }}</p>
      </div>
      <div v-else>
        <div class="CardData">
          <b>Host Info</b>

          <!-- Host Info -->
          <infogrid
            :infoItems="[{
              label: 'IP Address:', value: responseData.data.ipAddress
            }, {
              label: 'Is Public:', value: responseData.data.isPublic
            }, {
              label: 'IP Version:', value: responseData.data.ipVersion
            }, {
              label: 'Is Whitelisted:', value: responseData.data.isWhitelisted
            }]"
          />

          <hr class="w-full max-w-[600px] m-auto p-1" />

          <!-- Abuse Score and Additional Info -->
          <infogrid
            :infoItems="[{
              label: 'Abuse Score:', value: abuseScoreDisplay(), color: getAbuseScoreColour(responseData.data.abuseConfidenceScore)
            }, {
              label: 'Usage Type:', value: responseData.data.usageType
            }, {
              label: 'ISP:', value: responseData.data.isp
            }, {
              label: 'Domain:', value: responseData.data.domain
            }]"
          />

          <hr class="w-full max-w-[600px] m-auto p-1" />

          <!-- Tor, Country Info, and User Count -->
          <infogrid
            :infoItems="[{
              label: 'Country Name:', value: responseData.data.countryName
            }, {
              label: 'Users Num:', value: responseData.data.numDistinctUsers
            }]"
          />

          <hr class="w-full max-w-[600px] m-auto p-1" />

          <!-- Reports Section -->
          <div v-if="responseData.data.reports && responseData.data.reports.length > 1">
            <h3>Reports Per Day</h3>
            <canvas ref="reportsLineChart" class="w-full h-64 max-w-[400px] m-auto"></canvas>
          </div>

          <!-- Link to AbuseIPDB -->
          <div v-if="responseData.data.ipAddress !== 'status'">
            <a :href="`https://www.abuseipdb.com/check/${responseData.data.ipAddress}`" target="_blank">
              <CustomButtonNormal>Go to AbuseIPDB</CustomButtonNormal>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, nextTick, watch } from 'vue';
import { useFetchData } from '@scripts/useFetchData';
import infogrid from '@molecules/InfoGrid.vue';
import { Chart } from 'chart.js/auto'; // Import Chart.js
import CustomButtonNormal from '@atoms/CustomButtonNormal.vue';

export default defineComponent({
  name: 'AbuseIPDB',
  components: {
    infogrid,
    CustomButtonNormal,
  },
  props: {
    input: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const apiEndpoint = '/api/abuseipdb/request_data';
    const { loading, error, responseData } = useFetchData(apiEndpoint, props);
    const reportsLineChart = ref(null); // Ref for the chart

    const abuseScoreDisplay = () => {
      const score = responseData.value?.data?.abuseConfidenceScore;
      return score === 0
        ? `${score} % No Abuse Reported`
        : score < 30
        ? `${score} % Caution: Suspicious`
        : `${score} % Warning: Abusive`;
    };

    const getAbuseScoreColour = (score) => {
      return score === 0
        ? 'text-white bg-green-500 p-1 rounded-md'
        : score < 30
        ? 'text-white bg-orange-500 p-1 rounded-md'
        : 'text-white bg-red-500 p-1 rounded-md';
    };

    // Helper function to add missing dates
    const fillMissingDates = (reportDaysMap, startDate, endDate) => {
      let date = new Date(startDate);
      while (date <= new Date(endDate)) {
        const dateString = date.toISOString().split('T')[0];
        if (!reportDaysMap[dateString]) {
          reportDaysMap[dateString] = 0; // Fill in missing days with 0 reports
        }
        date.setDate(date.getDate() + 1);
      }
    };

    // Watch for changes in responseData and generate the line chart if there are more than 1 report
    watch(
      () => responseData.value?.data?.reports,
      (reports) => {
        if (reports && reports.length > 1) {
          nextTick(() => {
            createReportsLineChart();
          });
        }
      }
    );

    // Function to create the reports line chart by clumping reports per day and filling missing dates
    const createReportsLineChart = () => {
      const reports = responseData.value?.data?.reports;
      if (!reports || reports.length < 2 || !reportsLineChart.value) return;

      // Group reports by date (without time)
      const reportDaysMap = {};
      reports.forEach((report) => {
        const reportDate = new Date(report.reportedAt).toISOString().split('T')[0]; // Get only the date part (YYYY-MM-DD)
        reportDaysMap[reportDate] = (reportDaysMap[reportDate] || 0) + 1;
      });

      // Find the earliest and latest report date
      const dateLabels = Object.keys(reportDaysMap).sort();
      const startDate = dateLabels[0];
      const endDate = dateLabels[dateLabels.length - 1];

      // Fill in the missing dates with 0 reports
      fillMissingDates(reportDaysMap, startDate, endDate);

      const updatedDateLabels = Object.keys(reportDaysMap).sort(); // Updated with missing dates
      const reportCounts = Object.values(reportDaysMap); // Get counts for each day

      const ctx = reportsLineChart.value.getContext('2d');

      new Chart(ctx, {
  type: 'line',
  data: {
    labels: updatedDateLabels,
    datasets: [
      {
        label: 'Reports Per Day',
        data: reportCounts,
        borderColor: 'rgba(59, 130, 246, 1)',
        backgroundColor: 'rgba(59, 130, 246, 0.2)',
        fill: true,
        tension: 0.1,
      },
    ],
  },
  options: {
    responsive: true,
    animation: {
      duration: 1000, // 1 second smooth duration
      easing: 'easeInOutQuad', // Smooth transition
    },
    plugins: {
      legend: { display: false },
    },
    scales: {
      x: { title: { display: true, text: 'Date' } },
      y: { title: { display: true, text: 'Report Count' }, beginAtZero: true },
    },
  },
});


    };

    return {
      loading,
      error,
      responseData,
      abuseScoreDisplay,
      getAbuseScoreColour,
      reportsLineChart,
    };
  },
});
</script>

<style scoped>
/* Add Tailwind utility classes or additional custom styles here if needed */
</style>
