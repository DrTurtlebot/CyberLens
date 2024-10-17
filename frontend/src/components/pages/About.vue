<template>
  <div id="app" class="pt-20 p-2 pb-10 bg-zinc-50 dark:bg-zinc-900 dark:text-zinc-200 m-0 4k:p-6 4k:pb-16 animate-fadeInNoDelay transition-colors duration-400">
    <!-- Header Bar -->
    <CustomHeader
      :leftButtons="[
        { label: 'Home', route: '/', extraClasses: '' },
        { label: 'Report A Bug', route: '/bugreport', extraClasses: '' }
      ]"
    />

    <!-- Main Content -->
    <div id="header" class="relative max-w-3xl 4k:max-w-screen-2xl m-auto mt-4 p-2 text-center 4k:mt-24 4k:mb-10 4k:text-2xl">
      <b class="text-3xl dark:text-zinc-100 4k:text-6xl">About Cyberlens</b>
      
      <p class="mb-5"></p>

      <!-- Introduction -->
      <b class="text-2xl 4k:text-5xl">What is it?</b>
      <ul class="space-y-4">
          <div class="ml-4 4k:text-3xl" >
              <p>CyberLens is a web-based tool designed to assist cybersecurity analysts in investigating and analyzing suspicious IP addresses, domains, and file hashes. It aggregates data from multiple sources into a single, easy-to-use interface, highlighting pre-set rules and points of interest. CyberLens provides analysts with a broad overview of relevant information, allowing them to use other specialized tools to focus on specific threat indicators.</p>
          </div>

          <li><b class="4k:text-4xl ">Key Features</b></li>
          <div class="ml-4 text-left 4k:text-4xl ">
              <ul class="list-disc list-outside space-y-2">
                  <li><b>🔍 Data Aggregation:</b> Collects information from multiple data sources (e.g., APIs) and consolidates it into one unified interface for quick, comprehensive analysis.</li>
                  <li><b>🚨 Rule-based Highlighting:</b> Automatically flags suspicious activities and patterns using pre-set rules, helping analysts focus on what matters most.</li>
                  <li><b>📊 Visual Data Representation:</b> Offers clear and dynamic graphs of the data, helping analysts visualize trends, patterns, and anomalies.</li>
                  <li><b>🧠 AI Summary Reports:</b> Automatically generates summaries of findings using AI, giving analysts a high-level overview without the need to comb through raw data.</li>
                  <li><b>⚡ User-friendly Interface:</b> An intuitive design makes it simple to interpret complex data, helping users make quick and informed decisions.</li>
                  <li><b>📂 Image Export of Widgets:</b> Allows users to export graphs and widgets as images, making it easy to share and report findings.</li>
                  <li><b>🔗 Integration Ready:</b> CyberLens comes with its own API, allowing it to be integrated with other tools seamlessly. This enables cybersecurity analysts to call the CyberLens API for deeper threat analysis or to automate workflows.</li>
                  <li><b>🛠️ Customizable Alerts:</b> Set up custom alerts for emerging threats or user-defined triggers, ensuring timely responses to critical incidents.</li>
                  <li><b>🚀 Fast and Scalable:</b> Built for performance and scalability with a robust architecture using FastAPI and Docker.</li>
              </ul>
          </div>
      </ul>
    </div>
  </div>
</template>

<script>
import CustomHeader from '@organisms/CustomHeader.vue';
export default {
  name: 'About',
  components: {
    CustomHeader,
  },
};
</script>

<style scoped>
/* Tailwind classes handle most styling, adjust as needed */
</style>
