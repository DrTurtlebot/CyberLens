<template>
  <div class="4k:mt-8 4k:mb-8 4k:px-10">
    <p class="pb-3 dark:text-zinc-100 4k:text-3xl">Searching for {{ input }}</p>

    <!-- Display how many cards do not have the loading set to true out of the total cards -->
    <div v-if="cards.length > 0">
      <div class="flex flex-wrap flex-grow gap-2.5 justify-center items-start 4k:gap-6 4k:mt-4">
        <ModuleBox v-for="card in cards" :key="card" class="4k:scale-100 4k:mb-4 " :id="card">
          <component :is="card" :input="input" />
        </ModuleBox>
      </div>
    </div>
  </div>
</template>

  
  <script>
  import { ref, watch, defineComponent } from "vue";
  import ModuleBox from "@organisms/ModuleBox.vue";
  import AbuseIPDB from "@widgets/AbuseIPDB.vue";
  import ProxyCheck from "@widgets/ProxyCheck.vue";
  import NotRecognised from "@widgets/NotRecognised.vue";
  import VirusTotal from "@widgets/VirusTotal.vue";
  import UrlScanScreenshot from "@widgets/UrlScanScreenshot.vue";
  import Summary from "@widgets/Summary.vue";
  import Registrar from "@widgets/Registrar.vue";
  
  export default defineComponent({
    components: {
      ModuleBox,
      AbuseIPDB,
      ProxyCheck,
      NotRecognised,
      VirusTotal,
      UrlScanScreenshot,
      Summary,
      Registrar,
    },
    props: {
      input: {
        type: String,
        required: true,
      },
    },
    setup(props) {
      // Define the reactive state
      const cards = ref([]);
      const loading = ref(true);
      const error = ref(null);
      const responseData = ref(null);
      const viteBackendAddress = import.meta.env.VITE_BACKEND_ADDRESS || "http://localhost:4000"; // Access the environment variable here
      // Method to determine the input type and populate cards
      const populateCard = (data) => {
        loading.value = true;
        error.value = null;
        responseData.value = null;
        cards.value = [];
        console.log("Requesting Needed Cards");

  
        fetch(`${viteBackendAddress}/api/getcards/request_data`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("Network response was not ok");
            }
            return response.json();
          })
          .then((data) => {
            responseData.value = data;
            console.log("returned");
            console.log(data);
            cards.value = data;
          })
          .catch((err) => {
            error.value = err.message;
          })
          .finally(() => {
            loading.value = false;
          });
      };
  
      // Watch for changes in the input prop and call populateCard
      watch(
        () => props.input,
        (newValue) => {
          console.log("New input received:", newValue);
          populateCard(newValue);
        }
      );
  
      // Return the reactive properties and methods
      return {
        cards,
        viteBackendAddress,
      };
    },
  });
  </script>
  