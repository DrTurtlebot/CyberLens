<template>
  <!-- Main container -->
  <div
    id="app"
    class="main-app pt-20 p-2 pb-10 bg-zinc-50 dark:bg-zinc-900 dark:text-zinc-200 m-0
           4k:p-6 4k:pb-16 animate-fadeIn transition-colors duration-400"
  >
    <!-- HEADER (hidden before print) -->
    <CustomHeader
      id="headerBar"
      :leftButtons="[
        { label: 'About CyberLens', route: '/about', extraClasses: '' },
        { label: 'Report A Bug', route: '/bugreport', extraClasses: '' }
      ]"
    />

    <!-- INTRO SECTION (hidden before print) -->
    <div
      id="introSection"
      class="relative max-w-xl m-auto mt-4 p-2 text-center 4k:mt-24 4k:mb-10"
    >
      <b class="text-3xl dark:text-zinc-100 4k:text-6xl">CyberLens</b>
      <p>🐝 Ya like Jazz? 🎷</p>
    </div>

    <!-- SEARCH BAR (hidden before print) -->
    <div
      id="searchBar"
      class="relative max-w-xl 4k:max-w-6xl m-auto p-2 4k:mt-10 4k:mb-10"
    >
      <p class="text-md pt-3 dark:text-zinc-100 4k:text-5xl 4k:mt-6 4k:mb-4">
        Please Input An IP, URL, Domain or Hash...
      </p>
      <div class="flex">
        <input
          @keyup.enter="submitInput"
          v-model="input"
          type="text"
          placeholder="https://www.google.com... etc"
          class="relative m-0 -me-0.5 block flex-auto rounded-md border border-solid 
                 border-neutral-200 dark:border-zinc-600 bg-transparent bg-clip-padding px-3 py-1 
                 leading-[1.6] transition duration-200 ease-in-out placeholder:text-neutral-500 
                 focus:border-primary focus:shadow-inset focus:outline-none motion-reduce:transition-none 
                 dark:border_white/10 dark:autofill:shadow-autofill dark:focus:border-primary 
                 dark:placeholder:text-neutral-600 dark:bg-zinc-950 dark:text-white 
                 4k:py-4 4k:text-3xl transition-transform hover:scale-[1.02] hover:duration-[200ms]"
        />
        <button
          @click="submitInput"
          class="z-[2] inline-block rounded-e border-2 border-primary px-6 pb-[6px] pt-2 text-xs 
                 font-medium uppercase leading-normal text-primary transition duration-150 ease-in-out 
                 hover:border-primary-accent-300 hover:bg-primary-50/50 hover:text-primary-accent-300 
                 focus:border-primary-600 focus:pg-primary-50/50 focus:text-primary-600 focus:outline-none 
                 focus:ring-0 active:border-primary-700 active:text-primary-700 dark:hover:bg-zinc-950 
                 dark:focus:bg-zinc-950 dark:text-zinc-100 dark:border-zinc-600 4k:px-10 4k:py-4 
                 4k:text-lg 4k:mt-2 transition-transform hover:scale-[1.04] hover:duration-[200ms]"
          type="button"
        >
          Search
        </button>
      </div>
    </div>

    <!-- DATA SECTION (remains visible in print) -->
    <div id="dataContainer" class="4k:mt-12">
      <PopulateCards :input="submittedInput" />
    </div>

    <!-- PRINT BUTTON (hidden before print), only visible if submittedInput is non-empty -->
    <div
      id="printBtnContainer"
      class="flex justify-center mt-6"
      v-if="submittedInput"
    >
      <button
        @click="printPage"
        class="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition"
      >
        Print / Save as PDF (Experimental)
      </button>
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
    // Reactive references
    const input = ref('');
    const submittedInput = ref('');

    const route = useRoute();
    const router = useRouter();

    onMounted(() => {
      const param = route.params.searchParam;
      if (param) {
        input.value = param;
        submitInput(); // automatically search
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

    // 3) User triggers a search
    const submitInput = () => {
      if (input.value) {
        submittedInput.value = input.value;
        console.log('Submitted:', submittedInput.value);

        // Optionally update route param for shareable link
        router.push({
          name: 'Home',
          params: { searchParam: input.value },
        });
      }
    };

    const printPage = () => {
      const headerBar = document.getElementById('headerBar');
      const introSection = document.getElementById('introSection');
      const searchBar = document.getElementById('searchBar');
      const printBtnContainer = document.getElementById('printBtnContainer');

      // Hide them
      if (headerBar) headerBar.style.display = 'none';
      if (introSection) introSection.style.display = 'none';
      if (searchBar) searchBar.style.display = 'none';
      if (printBtnContainer) printBtnContainer.style.display = 'none';

      setTimeout(() => {
        window.print();
        // restore
        setTimeout(() => {
          if (headerBar) headerBar.style.display = '';
          if (introSection) introSection.style.display = '';
          if (searchBar) searchBar.style.display = '';
          if (printBtnContainer) printBtnContainer.style.display = '';
        }, 200);
      }, 200);
    };

    return {
      input,
      submittedInput,
      submitInput,
      printPage,
    };
  },
});
</script>

<style scoped>

/* Print styling */
@media print {
  .main-app {
    zoom: 0.7;
  }

  @page {
    size: A4;     
    margin: 10mm;  
  }

  .ModuleBox {
    page-break-before: always;
    break-before: page;
    page-break-inside: auto;
    break-inside: auto;
  }
}
</style>
