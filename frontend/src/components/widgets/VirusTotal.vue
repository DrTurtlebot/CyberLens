<template>
  <div>
    <b class="text-2xl 4k:text-5xl">Virus Total</b>

    <!-- Loading Spinner -->
    <div v-if="loading" class="flex items-center justify-center space-x-2">
      <span>Loading</span>
      <svg class="animate-spin h-5 w-5 text-black dark:text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.963 7.963 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>

    <p v-if="error">Error: {{ error }}</p>

    <!-- Virus Total Data -->
    <div v-if="responseData">
      <div v-if="responseData.error">
        <b class="text-white bg-red-500 p-1 max-w-[600px] m-auto block">Caution: Virus Total did not return any data or failed on the server side.</b>
      </div>
      <div v-else>
        <div class="CardData">
          <h3 class="text-lg 4k:text-4xl">Analysis Stats</h3>

          <!-- Chart for analysis stats -->
          <canvas v-if="responseData.analysis_stats" ref="analysisChartRef" class="mt-5 max-w-[250px] max-h-[250px] min-w-[250px] min-h-[250px] mx-auto block transition-transform transform ease-in-out duration-300 hover:scale-105"></canvas>

          <br><hr><br>

          <!-- Threat Status Labels -->
          <b v-if="responseData.analysis_stats.malicious === 0 && responseData.analysis_stats.suspicious === 0" class="text-white bg-green-500 p-1 m-auto block rounded-md">No Threat Detected</b>
          <b v-else-if="responseData.analysis_stats.malicious === 0 && responseData.analysis_stats.suspicious !== 0" class="text-white bg-orange-500 p-1 m-auto block rounded-md">Caution: Suspicious</b>
          <b v-else-if="responseData.analysis_stats.malicious !== 0" class="text-white bg-red-500 p-1 m-auto block rounded-md">Warning: Malicious Rating</b>

          <br>

          <!-- InfoGrid Component for Analysis Stats -->
          <infogrid
            :infoItems="[
              { label: 'Malicious:', value: responseData.analysis_stats.malicious, color: responseData.analysis_stats.malicious > 0 ? 'text-white bg-red-500 p-1 rounded-md' : '' },
              { label: 'Suspicious:', value: responseData.analysis_stats.suspicious, color: responseData.analysis_stats.suspicious > 0 ? 'text-white bg-orange-500 p-1 rounded-md' : '' },
              { label: 'Undetected:', value: responseData.analysis_stats.undetected },
              { label: 'Harmless:', value: responseData.analysis_stats.harmless },
              { label: 'Timeout:', value: responseData.analysis_stats.timeout },
              { label: 'Times Submitted:', value: responseData.times_submitted }
            ]"
          />

          <!-- Vote Stats -->
          <div v-if="responseData.all && (responseData.all.attributes.total_votes.harmless + responseData.all.attributes.total_votes.malicious) > 0">
            <hr class="w-full max-w-[600px] m-auto p-1 mt-2">
            <h3 class="text-lg 4k:text-4xl mt-4">Votes</h3>

            <!-- Chart for votes -->
            <canvas v-if="responseData.all && responseData.all.attributes.total_votes" ref="votesChartRef" class="mt-5 max-w-[250px] max-h-[250px] min-w-[250px] min-h-[250px] mx-auto block transition-transform transform ease-in-out duration-300 hover:scale-105"></canvas>

            <!-- InfoGrid Component for Votes -->
            <infogrid
              :infoItems="[
                { label: 'Harmless:', value: responseData.all.attributes.total_votes.harmless },
                { label: 'Malicious:', value: responseData.all.attributes.total_votes.malicious }
              ]"
            />
          </div>

          <div v-else>
            <h3>No Votes</h3>
          </div>

          <!-- Hash-Specific Info -->
          <div v-if="responseData.data_type === 'hash'">
            <hr class="w-full max-w-[600px] m-auto p-1 mt-2">
            <b>Hash Specific Info</b>

            <!-- InfoGrid Component for Hash Info -->
            <infogrid
              :infoItems="[
                { label: 'Meaningful Name:', value: responseData.all.attributes.meaningful_name },
                { label: 'Magic:', value: responseData.all.attributes.magic }
              ]"
            />


            <!-- Threat Categories -->
            <div v-if="responseData?.all?.attributes?.popular_threat_classification?.popular_threat_category">
            <hr class="w-full max-w-[600px] m-auto p-1 mt-2">
            <div class="InfoGrid">
              <div class="InfoLabel"><b>Threat Categories:</b></div>
              <div class="InfoValue">
                <ul>
                  <li v-for="(item, index) in responseData.all.attributes.popular_threat_classification.popular_threat_category" :key="index">
                    {{ item.count }} - {{ item.value }}
                  </li>
                </ul>
              </div>
            </div>
            </div>


            <!-- Threat Names -->
            <div v-if="responseData?.all?.attributes?.popular_threat_classification?.popular_threat_name">
              <hr class="w-full max-w-[600px] m-auto p-1 mt-2">
              <div class="InfoGrid">
              <div class="InfoLabel"><b>Threat Names:</b></div>
              <div class="InfoValue">
                <ul>
                  <li v-for="(item, index) in responseData.all.attributes.popular_threat_classification.popular_threat_name" :key="index">
                    {{ item.count }} - {{ item.value }}
                  </li>
                </ul>
              </div>
            </div>
            </div>

            <hr class="w-full max-w-[600px] m-auto p-1 mt-2">

            <!-- Type Tags -->
            <div class="InfoGrid">
              <div class="InfoLabel"><b>Type Tags:</b></div>
              <div class="InfoValue">
                <ul>
                  <li v-for="ns in responseData.all.attributes.type_tags" :key="ns">
                    {{ ns }}
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Link to VirusTotal -->
          <a :href="`https://www.virustotal.com/gui/search/${responseData.raw_input}`" target="_blank">
            <CustomButtonNormal>Go to VirusTotal</CustomButtonNormal>
          </a>
        </div>
      </div>
    </div>
    <div v-else>
      <p>No Data Returned</p>
    </div>
    
  </div>
</template>

<script>
import { defineComponent, ref, watch, nextTick } from 'vue';
import { useFetchData } from '@scripts/useFetchData';
import { Chart } from 'chart.js/auto';
import infogrid from '@molecules/InfoGrid.vue'; // Import InfoGrid component
import CustomButtonNormal from '@atoms/CustomButtonNormal.vue'; // Import CustomButtonNormal component

export default defineComponent({
  name: 'VirusTotal',
  components: {
    infogrid, // Register the InfoGrid component
    CustomButtonNormal, // Register the CustomButtonNormal component
  },
  props: {
    input: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const apiEndpoint = '/api/virustotal/request_data';
    const { loading, error, responseData } = useFetchData(apiEndpoint, props);

    // Refs for both canvas elements
    const analysisChartRef = ref(null);
    const votesChartRef = ref(null);

    // Function to create the Analysis Chart
    const createAnalysisChart = () => {
      if (!analysisChartRef.value || !responseData.value?.analysis_stats) return;

      const ctx = analysisChartRef.value.getContext('2d');
      const stats = responseData.value.analysis_stats;
      const data = [stats.malicious, stats.suspicious, stats.undetected, stats.harmless, stats.timeout];

      new Chart(ctx, {
        type: 'pie',
        data: {
          labels: ['Malicious', 'Suspicious', 'Undetected', 'Harmless', 'Timeout'],
          datasets: [{
            data,
            backgroundColor: [
              'rgba(230, 2, 2, 0.3)',    // Red with 30% opacity
              'rgba(252, 149, 5, 0.3)',  // Orange with 30% opacity
              'rgba(0, 183, 255, 0.3)',  // Blue with 30% opacity
              'rgba(26, 255, 0, 0.3)',   // Green with 30% opacity
              'rgba(228, 201, 255, 0.3)' // Light Purple with 30% opacity
            ],
            borderColor: [
              'rgba(230, 2, 2, 1)',      // Solid Red
              'rgba(252, 149, 5, 1)',    // Solid Orange
              'rgba(0, 183, 255, 1)',    // Solid Blue
              'rgba(26, 255, 0, 1)',     // Solid Green
              'rgba(228, 201, 255, 1)'   // Solid Light Purple
            ],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false },
            title: { display: false }
          }
        }
      });
    };

    // Function to create the Votes Chart
    const createVotesChart = () => {
      if (!votesChartRef.value || !responseData.value?.all?.attributes.total_votes) return;

      const ctx = votesChartRef.value.getContext('2d');
      const votes = responseData.value.all.attributes.total_votes;
      const data = [votes.harmless, votes.malicious];

      new Chart(ctx, {
        type: 'pie',
        data: {
          labels: ['Harmless', 'Malicious'],
          datasets: [{
            data,
            backgroundColor: [
              'rgba(26, 255, 0, 0.3)',   // Green with 30% opacity
              'rgba(230, 2, 2, 0.3)'     // Red with 30% opacity
            ],
            borderColor: [
              'rgba(26, 255, 0, 1)',     // Solid Green
              'rgba(230, 2, 2, 1)'       // Solid Red
            ],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false },
            title: { display: false }
          },
          animation: {
            duration: 1000, // 1 second
            easing: 'easeOutQuart',
            animateRotate: true, // Enable rotation animation
            animateScale: true // Enable scaling animation
          }
        },
  
      });
    };

    // Watch for responseData to trigger chart creation
    watch(responseData, () => {
      nextTick(() => {
        if (analysisChartRef.value) {
          createAnalysisChart();
        }
        if (votesChartRef.value) {
          createVotesChart();
        }
      });
    });

    return {
      loading,
      error,
      responseData,
      analysisChartRef,
      votesChartRef,
    };
  },
});
</script>

<style scoped>
/* Add Tailwind utility classes for scoped styling if needed */
</style>
