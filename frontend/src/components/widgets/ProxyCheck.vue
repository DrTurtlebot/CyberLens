<template>
  <div>
    <b class="text-2xl 4k:text-5xl">Proxy Check</b>
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
          <div v-if="responseData.status !== 'denied'">
            <div v-for="(proxyValue, ip) in responseData" :key="ip">
              <div v-if="ip !== 'status' && ip !== 'message'">
                <b class="text-lg 4k:text-4xl">Host Info</b>
                <!-- Host Info Section -->
                <infogrid
                  :infoItems="[
                    { label: 'IP:', value: ip },
                    { label: 'Hostname:', value: proxyValue.hostname },
                    { label: 'Provider:', value: proxyValue.provider },
                    { label: 'Proxy:', value: proxyValue.proxy }
                  ]"
                />
                
                <hr class="w-full max-w-[600px] m-auto p-1">

                <!-- Location Section -->
                <b class="text-xl mt-4">Location</b>
                <infogrid
                  :infoItems="[
                    { label: 'Continent:', value: proxyValue.continent },
                    { label: 'Country:', value: proxyValue.country },
                    { label: 'Region:', value: proxyValue.region },
                    { label: 'City:', value: proxyValue.city },
                    { label: 'Latitude:', value: proxyValue.latitude },
                    { label: 'Longitude:', value: proxyValue.longitude }
                  ]"
                />
                
                <hr class="w-full max-w-[600px] m-auto p-1">

                <!-- Specifics Section -->
                <b class="text-xl mt-4">Specifics</b>
                <infogrid
                  :infoItems="[
                    { label: 'ASN:', value: proxyValue.asn },
                    { label: 'Range:', value: proxyValue.range },
                    { label: 'Proxy:', value: proxyValue.proxy },
                    { label: 'Type:', value: proxyValue.type }
                  ]"
                />
              </div>

              <!-- Error message for unexpected responses -->
              <div v-else-if="ip == 'message'">
                <p>Proxy Check sent back a different response than expected</p>
                <p>Reason: <b> {{ responseData.message }}</b></p>
              </div>

              <!-- Link to ProxyCheck for further details -->
              <a v-if="ip != 'status'" :href="`https://proxycheck.io/v2/${ip}?vpn=1&asn=1`" target="_blank">
                <CustomButtonNormal @click="copyContent">Go to ProxyCheck</CustomButtonNormal>
              </a>
            </div>
          </div>

          <!-- Denied Response Handling -->
          <div v-else class="InfoValue">
            <p>Oh no, this module denied to send back data</p>
            <p>Reason: {{ responseData.message }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import { useFetchData } from '@scripts/useFetchData';
import infogrid from '@molecules/InfoGrid.vue'; // Correct import of infogrid component
import CustomButtonNormal from '@atoms/CustomButtonNormal.vue'; // Correct import of CustomButtonNormal component

export default defineComponent({
  name: 'ProxyCheck',
  components: {
    infogrid, // Register the infogrid component
    CustomButtonNormal, // Register the CustomButtonNormal component
  },
  props: {
    input: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const apiEndpoint = '/api/proxycheck/request_data';
    const { loading, error, responseData } = useFetchData(apiEndpoint, props);

    return {
      loading,
      error,
      responseData,
    };
  },
});
</script>
