<template>
    <div>
        <b class="text-2xl 4k:text-5xl">ScreenShot</b>
        <p>Via UrlScan.io</p>
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
                    <img :src="responseData.screenshot_url" alt="screenshot" class="m-auto max-w-full  "/>
                    <h3></h3>
                </div>       
            </div>
        </div> 
    </div>
</template>

<script>
import { defineComponent, ref } from 'vue';
import { useFetchData } from '@scripts/useFetchData';

export default defineComponent({
    name: 'AbuseIPDB',
    props: {
        input: {
            type: String,
            required: true,
        },
    },
    setup(props) {
        const apiEndpoint = '/api/urlscan/screenshot';
        const { loading, error, responseData } = useFetchData(apiEndpoint, props);
        const selectedReportIndex = ref(null);

        return {
            loading,
            error,
            responseData,
            selectedReportIndex,
        };
    },
});
</script>
