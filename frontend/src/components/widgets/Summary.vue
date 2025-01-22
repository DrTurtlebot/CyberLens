<template>
  <div>
    <b class="text-2xl 4k:text-5xl">Summary</b>
    <div v-if="loading" class="flex items-center justify-center space-x-2">
      <span>Loading</span>
      <svg class="animate-spin h-5 w-5 text-black dark:text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.963 7.963 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>
    <div v-else>
      <p v-if="error">Error: {{ error }}</p>

      <div v-if="responseData">
        <div v-if="responseData.Error">
          <p>Error: {{ responseData.Error }}</p>
        </div>
        <div v-else>
          <div class="CardData">

            <b class="text-lg 4k:text-4xl">Summary of Info</b>

            <!-- Conflict in IP Section -->
            <div v-if="responseData.Abuse_IP !== responseData.Proxy_IP">
              <b class="text-white bg-red-500 p-1 w-full max-w-[600px] m-auto block">Conflict In IP</b>
              <infogrid
                :infoItems="[
                  { label: 'Abuse IP:', value: responseData.Abuse_IP },
                  { label: 'Proxy IP:', value: responseData.Proxy_IP }
                ]"
              />
            </div>
            <div v-else>
              <infogrid
                :infoItems="[
                  { label: 'IP:', value: responseData.Abuse_IP }
                ]"
              />
            </div>

            <!-- ISP Info -->
            <infogrid
              :infoItems="[
                { label: 'ISP:', value: responseData.Abuse_ISP }
              ]"
            />

            <hr class="w-full max-w-[600px] m-auto p-1">

            <!-- Proxy Detected Section -->
            <div v-if="responseData.Proxy_Proxy !== 'no'">
              <b class="text-white bg-blue-500 p-1 w-full max-w-[600px] m-auto block">Info: Proxy Detected</b>
            </div>
            <infogrid
              :infoItems="[
                { label: 'Proxy:', value: responseData.Proxy_Proxy },
                { label: 'Connection Type:', value: responseData.Proxy_Type }
              ]"
            />

            <!-- Conflict of Location Section -->
            <!-- These are chunky as they have lots of fall backs depending on what modules were sent. -->
            <div v-if="responseData.Proxy_ISOCountry || responseData.Abuse_CountryCode">
              <div v-if="responseData.Abuse_CountryCode && responseData.Proxy_ISOCountry">
                <!-- If both AbuseIPDB and Proxy data are present, check for conflict -->
                <div v-if="responseData.Abuse_CountryCode !== responseData.Proxy_ISOCountry">
                  <b class="text-white bg-orange-500 p-1 w-full max-w-[600px] m-auto block rounded-md">
                    Caution: Conflict of Location
                  </b>
                  <infogrid
                    :infoItems="[
                      { label: 'Abuse Country Code:', value: responseData.Abuse_CountryCode, color: 'text-white bg-red-500 p-1 rounded-md' },
                      { label: 'Abuse Country Name:', value: responseData.Abuse_CountryName, color: 'text-white bg-red-500 p-1 rounded-md' },
                      { label: 'Proxy Country Code:', value: responseData.Proxy_ISOCountry, color: 'text-white bg-red-500 p-1 rounded-md' },
                      { label: 'Proxy Country Name:', value: responseData.Proxy_Country, color: 'text-white bg-red-500 p-1 rounded-md' },
                      { label: 'City:', value: responseData.Proxy_City }
                    ]"
                  />
                </div>
                <div v-else>
                  <!-- If no conflict, prioritize AbuseIPDB info and show Proxy city -->
                  <hr class="w-full max-w-[600px] m-auto">
                  <infogrid
                    :infoItems="[
                      { label: 'Country Code:', value: responseData.Abuse_CountryCode },
                      { label: 'Country Name:', value: responseData.Abuse_CountryName },
                      { label: 'City:', value: responseData.Proxy_City }
                    ]"
                  />
                </div>
              </div>

              <!-- If only AbuseIPDB info is available -->
              <div v-else-if="responseData.Abuse_CountryCode">
                <hr class="w-full max-w-[600px] m-auto">
                <infogrid
                  :infoItems="[
                    { label: 'Country Code:', value: responseData.Abuse_CountryCode },
                    { label: 'Country Name:', value: responseData.Abuse_CountryName }
                  ]"
                />
              </div>

              <!-- If only ProxyCheck info is available -->
              <div v-else-if="responseData.Proxy_ISOCountry">
                <hr class="w-full max-w-[600px] m-auto">
                <infogrid
                  :infoItems="[
                    { label: 'Country Code:', value: responseData.Proxy_ISOCountry },
                    { label: 'Country Name:', value: responseData.Proxy_Country },
                    { label: 'City:', value: responseData.Proxy_City }
                  ]"
                />
              </div>
            </div>
            <!-- Abuse Score Section -->
            <div v-if="responseData.Abuse_Score !== undefined && responseData.Abuse_Score !== null">
              <hr class="w-full max-w-[600px] m-auto p-1" />
              <infogrid
                :infoItems="[
                  { 
                    label: 'Abuse Score:', 
                    value: `${responseData.Abuse_Score} %`, 
                    color: responseData.Abuse_Score > 30 
                      ? 'text-white bg-red-500 p-1 rounded-md' 
                      : responseData.Abuse_Score > 0 
                        ? 'text-white bg-orange-500 p-1 rounded-md' 
                        : 'text-white bg-green-500 p-1 rounded-md'  
                  },
                ]"
              />
            </div>
            <hr class="w-full max-w-[600px] m-auto p-1">
            <!-- Virus Total Section -->
            <div v-if="responseData.Virus_Error">
              <b class="text-white bg-orange-500 p-1 w-full max-w-[600px] m-auto block">Caution: Virus Total Did not Return Any Data</b>
            </div>
            <div v-else>
              <b> Virus Total </b>
              <div v-if="responseData.Virus_Stats.malicious > 4">
                <b class="text-white bg-red-500 p-1 w-full max-w-[600px] m-auto block rounded-md">Warning: Malicious Rating</b>
              </div>
              <div v-else-if="responseData.Virus_Stats.suspicious > 0 || responseData.Virus_Stats.malicious > 0">
                <b class="text-white bg-orange-500 p-1 w-full max-w-[600px] m-auto block rounded-md">Caution: Suspicious Rating</b>
              </div>
              <infogrid
                :infoItems="[
                  { label: 'Malicious:', value: responseData.Virus_Stats.malicious },
                  { label: 'Suspicious:', value: responseData.Virus_Stats.suspicious },
                  { label: 'Undetected:', value: responseData.Virus_Stats.undetected },
                  { label: 'Harmless:', value: responseData.Virus_Stats.harmless },
                  { label: 'Timeout:', value: responseData.Virus_Stats.timeout }
                ]"
              />
            </div>

            <!-- Abuse Reports Section -->
            <div v-if="responseData.Abuse_Reports > 0">
              <hr class="w-full max-w-[600px] m-auto p-1">
              <b v-if="responseData.Abuse_Reports > 5" class="text-white bg-red-500 p-1 w-full max-w-[600px] m-auto block">Warning: Abuse Reports</b>
              <b v-else class="text-white bg-orange-500 p-1 w-full max-w-[600px] m-auto block">Caution: Abuse Reports</b>
              <infogrid
                :infoItems="[
                  { label: 'Abuse Reports:', value: responseData.Abuse_Reports }
                ]"
              />
            </div>

            <!-- Registrar Info Section -->
            <div v-if="responseData.Registrar_Error">
              <b class="text-white bg-blue-500 p-1 w-full max-w-[600px] m-auto block">Caution: Not all Registrar Data was Received</b>
            </div>
            <div v-else>
              <hr class="w-full max-w-[600px] m-auto p-1">
              <infogrid
                :infoItems="[
                  { label: 'Registrar Name:', value: responseData.Registrar_Name },
                  { label: 'Registrar WhoIs:', value: responseData.Registrar_WHOIS },
                  { label: 'Created Date:', value: formatDateTime(responseData.Registrar_Created) },
                  { label: 'Updated Date:', value: formatDateTime(responseData.Registrar_Updated) },
                  { label: 'Expiration Date:', value: formatDateTime(responseData.Registrar_Expire) }
                ]"
              />
              <div v-if="responseData.Registrar_Data_Found === false">
                <b class="text-white bg-blue-500 p-1 w-full max-w-[600px] m-auto block">Info: No Registrant Specific Data Found</b>
              </div>
            </div>
          </div>

          <!-- Report Generation Button -->
          <div id="SummaryPdfRequest">
            <CustomButtonNormal class="disabled:bg-gray-400 disabled:cursor-not-allowed" :disabled="isGeneratingReport" @click="generateReport">
              <svg v-if="isGeneratingReport" class="animate-spin h-5 w-5 text-white mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.963 7.963 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span v-if="isGeneratingReport">Generating...</span>
              <span v-else>Download AI PDF Report</span>
            </CustomButtonNormal>
          </div>
        </div>
      </div>
      <div v-else>
        <p>No Data Returned</p>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue';
import { useFetchData } from '@scripts/useFetchData';
import infogrid from '@molecules/InfoGrid.vue'; // Ensure correct import of infogrid component
import CustomButtonNormal from '@atoms/CustomButtonNormal.vue';

export default defineComponent({
  name: 'Summary',
  components: {
    infogrid, // Register the infogrid component
    CustomButtonNormal,
  },
  props: {
    input: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const apiEndpoint = '/api/summary/request_data';
    const { loading, error, responseData } = useFetchData(apiEndpoint, props);
    const isGeneratingReport = ref(false);

    const viteBackendAddress = import.meta.env.VITE_BACKEND_ADDRESS || "http://localhost:4000"; // Access the environment variable here

    const formatDateTime = (dateString) => {
      if (!dateString) return 'N/A';
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    };

    const generateReport = async () => {
      isGeneratingReport.value = true;
      const timeout = setTimeout(() => {
        alert('Failed to download the report. Please try again after 30 seconds.');
        isGeneratingReport.value = false;
      }, 60000);

      try {
        const response = await fetch(`${viteBackendAddress}/api/summary/generate_report`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(props.input),
        });

        clearTimeout(timeout);

        if (!response.ok) throw new Error('Failed to generate report.');

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'CyberLens_Report.pdf';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error('Error generating report:', error);
        alert('Failed to download the report. Please try again.');
      } finally {
        isGeneratingReport.value = false;
      }
    };

    return {
      loading,
      error,
      responseData,
      formatDateTime,
      generateReport,
      isGeneratingReport,
    };
  },
});
</script>

<style scoped>
/* Add Tailwind utility classes for scoped styling if needed */
</style>
