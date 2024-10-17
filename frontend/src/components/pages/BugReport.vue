<template>
  <div
    id="app"
    class="pt-20 p-2 pb-10 bg-zinc-50 dark:bg-zinc-900 dark:text-zinc-200 m-0 4k:pt-40 4k:p-6 4k:pb-16 animate-fadeInNoDelay transition-colors duration-400"
  >
    <!-- Header Bar -->
     <CustomHeader
      :leftButtons="[
        { label: 'Home', route: '/', extraClasses: '' },
        { label: 'Report A Bug', route: '/bugreport', extraClasses: '' }
      ]"
    />

    <!-- Main Content -->
    <div id="header" class="relative max-w-xl m-auto mt-4 p-2 text-center 4k:mt-24 4k:mb-10 4k:text-lg">
      <b class="text-3xl dark:text-zinc-100 4k:text-6xl">Report a Bug</b>
      <p class="4k:text-2xl">Welcome to the Bug Reporter</p>
      <p class="text-neutral-300 dark:text-neutral-500 4k:text-lg">(Please do not include any confidential information or sensitive personal info)</p>

      <!-- Bug Report Form -->
      <form @submit.prevent="submitBugReport" class="mt-6 4k:mt-12">
        <!-- Name (Optional) -->
        <div class="mb-4 4k:mb-8">
          <label for="name" class="block text-sm font-medium dark:text-zinc-100 text-left 4k:text-lg">Name (Optional):</label>
          <input
            v-model="bugReport.name"
            type="text"
            id="name"
            placeholder="Your name"
            class="mt-1 block w-full rounded-md border border-gray-300 dark:border-zinc-600 bg-zinc-50 dark:bg-zinc-800 px-3 py-2 focus:outline-none focus:ring-1 focus:ring-primary dark:text-zinc-100 4k:px-6 4k:py-4"
          />
        </div>

        <!-- Email (Optional) -->
        <div class="mb-4 4k:mb-8">
          <label for="email" class="block text-sm font-medium dark:text-zinc-100 text-left 4k:text-lg">Email (Optional):</label>
          <input
            v-model="bugReport.email"
            type="email"
            id="email"
            placeholder="Your email"
            class="mt-1 block w-full rounded-md border border-gray-300 dark:border-zinc-600 bg-zinc-50 dark:bg-zinc-800 px-3 py-2 focus:outline-none focus:ring-1 focus:ring-primary dark:text-zinc-100 4k:px-6 4k:py-4"
          />
        </div>

        <!-- URL or IP Address -->
        <div class="mb-4 4k:mb-8">
          <label for="urlOrIp" class="block text-sm font-medium dark:text-zinc-100 text-left 4k:text-lg">URL/IP Address (Optional):</label>
          <input
            v-model="bugReport.urlOrIp"
            type="text"
            id="urlOrIp"
            placeholder="URL or IP where the bug occurred"
            class="mt-1 block w-full rounded-md border border-gray-300 dark:border-zinc-600 bg-zinc-50 dark:bg-zinc-800 px-3 py-2 focus:outline-none focus:ring-1 focus:ring-primary dark:text-zinc-100 4k:px-6 4k:py-4"
          />
        </div>

        <!-- Bug Description -->
        <div class="mb-4 4k:mb-8">
          <label for="description" class="block text-sm font-medium dark:text-zinc-100 text-left 4k:text-lg">Bug Description:</label>
          <textarea
            v-model="bugReport.description"
            id="description"
            rows="5"
            placeholder="Describe the issue you encountered..."
            required
            class="mt-1 block w-full rounded-md border border-gray-300 dark:border-zinc-600 bg-zinc-50 dark:bg-zinc-800 px-3 py-2 focus:outline-none focus:ring-1 focus:ring-primary dark:text-zinc-100 4k:px-6 4k:py-4"
          ></textarea>
        </div>

        <!-- Submit Button -->
        <div class="text-center">
          <button
            type="submit"
            class="px-6 py-2 bg-primary text-black bg-white rounded-md transition-transform hover:scale-[1.04] hover:bg-primary-accent-300 focus:outline-none dark:bg-black dark:text-white 4k:px-10 4k:py-4 4k:text-lg"
          >
            Submit Bug Report
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import CustomHeader from '@organisms/CustomHeader.vue';

export default {
  name: 'BugReport',
  components: {
    CustomHeader
  },
  data() {
    return {
      bugReport: {
        name: '',
        email: '',
        url_or_ip: '',  // Ensure this is snake_case
        description: '',
      },
    };
  },
  methods: {
    async submitBugReport() {
      try {
        // Log what you're sending to make sure it's correct
        console.log('Sending Bug Report:', JSON.stringify(this.bugReport, null, 2));

        const viteBackendAddress = import.meta.env.VITE_BACKEND_ADDRESS || "http://localhost:4000"; // Access the environment variable here
        const response = await fetch(`${viteBackendAddress}/api/bug-report/report`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.bugReport, null, 2),
        });

        if (!response.ok) {
          throw new Error('Failed to submit bug report');
        }

        const data = await response.json();
        alert('Bug report submitted successfully!');
        console.log('Response:', data);
      } catch (error) {
        console.error('Error submitting bug report:', error);
        alert('There was an issue submitting the bug report.');
      }
    },
  },
};
</script>


<style scoped>
/* Tailwind classes handle most styling, adjust as needed */
</style>
