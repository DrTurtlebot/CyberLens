<template>
  <div>
    <b class="text-2xl 4k:text-5xl">Registrar</b>
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
          <!-- Registrar Info Section -->
          <b class="text-lg 4k:text-4xl">Registrar Info</b>
          <infogrid
            :infoItems="[
              { label: 'Registrar:', value: responseData.registrar.name },
              { label: 'Registrar URL:', value: responseData.registrar.referral_url },
              { label: 'WhoIs Server:', value: responseData.domain.whois_server },
              { label: 'Date Created:', value: formatDateTime(responseData.domain.created_date_in_time) },
              { label: 'Date Updated:', value: formatDateTime(responseData.domain.updated_date_in_time) },
              { label: 'Date of Expiration:', value: formatDateTime(responseData.domain.expiration_date) }
            ]"
          />

          <!-- Name Servers Section -->
          <div v-if="responseData.domain.name_servers">
            <infogrid
              :infoItems="[
                { label: 'Name Servers:', value: '' }
              ]"
            />
            <ul class="ml-4 mr-10 text-right">
              <li v-for="ns in responseData.domain.name_servers" :key="ns">{{ ns }}</li>
            </ul>
          </div>

          <!-- Registrant Section -->
          <div v-if="responseData.registrant">
            <hr class="w-full max-w-[600px] m-auto p-1 mt-2" />
            <infogrid
              :infoItems="[
                { label: 'Organisation:', value: responseData.registrant.organization },
                { label: 'Country:', value: responseData.registrant.country },
                { label: 'Province:', value: responseData.registrant.province },
                { label: 'Email:', value: responseData.registrant.email },
                { label: 'Registrar Abuse Email:', value: responseData.registrar.email }
              ]"
            />
          </div>
          <div v-else>
            <b class="text-white bg-blue-500 p-1 w-full max-w-[600px] m-auto block">Info: No Registrant Specific Data Found</b>
          </div>

          <hr class="w-full max-w-[600px] m-auto p-1 mt-2" />

          <!-- Status Section -->
          <infogrid
            :infoItems="[
              { label: 'Status:', value: '' }
            ]"
          />
          <ul class="ml-4 mr-10 text-right">
            <li v-for="ns in responseData.domain.status" :key="ns">{{ ns }}</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue';
import { useFetchData } from '@scripts/useFetchData';
import infogrid from '@molecules/InfoGrid.vue'; // Ensure correct import of infogrid component

export default defineComponent({
  name: 'Registrar',
  components: {
    infogrid, // Register the infogrid component
  },
  props: {
    input: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const apiEndpoint = '/api/registrar/request_data';
    const { loading, error, responseData } = useFetchData(apiEndpoint, props);
    const selectedReportIndex = ref(null);

    // Date formatting function to convert ISO strings into readable formats
    const formatDateTime = (dateString) => {
      if (!dateString) return 'N/A';
      const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      };
      return new Date(dateString).toLocaleDateString(undefined, options);
    };

    return {
      loading,
      error,
      responseData,
      selectedReportIndex,
      formatDateTime,
    };
  },
});
</script>
