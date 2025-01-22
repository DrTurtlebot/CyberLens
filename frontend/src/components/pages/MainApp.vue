<template>
  <div
    id="app"
    class="pt-20 p-2 pb-10 bg-zinc-50 dark:bg-zinc-900 dark:text-zinc-200 m-0 4k:p-6 4k:pb-16 animate-fadeIn transition-colors duration-400"
  >
    <!-- Header Bar -->
    <CustomHeader
      :leftButtons="[
        { label: 'About CyberLens', route: '/about', extraClasses: '' },
        { label: 'Report A Bug', route: '/bugreport', extraClasses: '' }
      ]"
    />

    <!-- Main Content -->
    <div
      id="header"
      class="relative max-w-xl m-auto mt-4 p-2 text-center 4k:mt-24 4k:mb-10"
    >
      <b class="text-3xl dark:text-zinc-100 4k:text-6xl">CyberLens</b>
      <p>🐝 Ya like Jazz? 🎷</p>
    </div>

    <!-- Search Bar -->
    <div id="Search Bar" class="relative max-w-xl 4k:max-w-6xl m-auto p-2 4k:mt-10 4k:mb-10">
      <p class="text-md pt-3 dark:text-zinc-100 4k:text-5xl 4k:mt-6 4k:mb-4">Please Input An IP, URL, Domain or Hash...</p>
      <div class="flex">
        <input
          @keyup.enter="submitInput"
          v-model="input"
          type="text"
          id="input"
          placeholder="https://www.google.com... etc"
          class="relative m-0 -me-0.5 block flex-auto rounded-md border border-solid border-neutral-200 dark:border-zinc-600 bg-transparent bg-clip-padding px-3 py-1 leading-[1.6] transition duration-200 ease-in-out placeholder:text-neutral-500 focus:border-primary focus:shadow-inset focus:outline-none motion-reduce:transition-none dark:border_white/10 dark:autofill:shadow-autofill dark:focus:border-primary dark:placeholder:text-neutral-600 dark:bg-zinc-950 dark:text-white 4k:py-4 4k:text-3xl transition-transform hover:scale-[1.02] hover:duration-[200ms]"
        />
        <button
          id="SubmitRequest"
          @click="submitInput"
          class="z-[2] inline-block rounded-e border-2 border-primary px-6 pb-[6px] pt-2 text-xs font-medium uppercase leading-normal text-primary transition duration-150 ease-in-out hover:border-primary-accent-300 hover:bg-primary-50/50 hover:text-primary-accent-300 focus:border-primary-600 focus:pg-primary-50/50 focus:text-primary-600 focus:outline-none focus:ring-0 active:border-primary-700 active:text-primary-700 dark:hover:bg-zinc-950 dark:focus:bg-zinc-950 dark:text-zinc-100 dark:border-zinc-600 4k:px-10 4k:py-4 4k:text-lg 4k:mt-2 transition-transform hover:scale-[1.04] hover:duration-[200ms]"
          type="button"
        >
          Search
        </button>
      </div>
    </div>

    <!-- Data Display Section -->
    <div id="Data arrived" class="4k:mt-12">
      <!-- Pass the submitted input value to PopulateCards -->
      <PopulateCards :input="submittedInput" />
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import PopulateCards from '@organisms/PopulateCards.vue';
import CustomHeader from '@organisms/CustomHeader.vue';

export default defineComponent({
  name: 'MainApp',
  components: {
    PopulateCards,
    CustomHeader,
  },
  setup() {
    const route = useRoute();
    const router = useRouter();

    const input = ref('');
    const submittedInput = ref('');

    const isIpAddress = (value) => {
      const ipPattern =
        /^(25[0-5]|2[0-4]\d|[01]?\d?\d)\.(25[0-5]|2[0-4]\d|[01]?\d?\d)\.(25[0-5]|2[0-4]\d|[01]?\d?\d)\.(25[0-5]|2[0-4]\d|[01]?\d?\d)$/;
      return ipPattern.test(value);
    };

    const isHash = (value) => {
      // Matches common hash lengths: 32 (MD5), 40 (SHA1), 64 (SHA256)
      const hashPattern = /^[a-fA-F0-9]{32}$|^[a-fA-F0-9]{40}$|^[a-fA-F0-9]{64}$/;
      return hashPattern.test(value);
    };

    const formatUrl = (value) => {
      // Remove whitespace
      value = value.replace(/\s/g, '');

      // If IP address or recognized hash, return as-is
      if (isIpAddress(value) || isHash(value)) {
        return value;
      }

      // URL pattern check
      const urlPattern = /^(https?:\/\/)?([\w-]+\.)+\w{2,}(\/.*)?$/;
      const hasProtocol = /^https?:\/\//.test(value);

      if (urlPattern.test(value)) {
        return hasProtocol ? value : `http://${value}`;
      }

      // Fallback
      return `http://www.${value}`;
    };
    const submitInput = () => {
      if (input.value) {
        // Format the user input (e.g., add http:// if missing)
        submittedInput.value = formatUrl(input.value);
        console.log('Submitted:', submittedInput.value);

        // Optional: Update the URL param so the user can share the link
        // e.g. /google.com
        router.push({
          name: 'Home',
          params: { searchParam: input.value },
        });
      }
    };

    // set our input and perform a search
    onMounted(() => {
      const param = route.params.searchParam;
      if (param) {
        input.value = param;
        submitInput();
      }
    });

    watch(
      () => route.params.searchParam,
      (newVal, oldVal) => {
        if (newVal && newVal !== oldVal) {
          input.value = newVal;
          submitInput();
        }
      }
    );

    return {
      input,
      submittedInput,
      submitInput,
    };
  },
});
</script>


<style scoped>
/* Tailwind classes handle most styling, adjust as needed */
</style>
