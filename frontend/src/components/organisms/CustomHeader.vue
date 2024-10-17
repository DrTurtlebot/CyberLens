<template>
  <header class="fixed top-0 left-0 right-0 z-50 flex justify-between items-center p-4 bg-zinc-50 dark:bg-zinc-900 transition-colors duration-400">
    <!-- Left Side Buttons -->
    <div class="flex items-center space-x-4">
      <router-link v-for="button in leftButtons" :key="button.label" :to="button.route">
        <button
          :class="button.extraClasses || defaultButtonClass"
        >
          {{ button.label }}
        </button>
      </router-link>
    </div>

    <!-- Right Side Components - Theme Switcher integrated here -->
    <div class="flex items-center space-x-4">
      <!-- Dark Mode Toggle Button -->
      <button
        @click="toggleDarkMode"
        id="DarkModeToggle"
        :class="[
          isDarkMode ? 'bg-black text-white' : 'bg-white text-black',
          'py-2 px-4 rounded max-w-[200px] 4k:py-4 4k:px-8 4k:text-xl'
        ]"
      >
        {{ isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode' }}
      </button>
    </div>
  </header>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  props: {
    leftButtons: {
      type: Array,
      required: true,
      default: () => [],
    },
  },
  setup() {
    const isDarkMode = ref(false);
    const selectedTheme = ref('default');

    const themes = ref([
      { name: 'default', colors: { '--primary-color': '#007bff', '--secondary-color': '#6c757d' }},
      { name: 'red', colors: { '--primary-color': '#dc3545', '--secondary-color': '#6c757d' }},
      { name: 'green', colors: { '--primary-color': '#28a745', '--secondary-color': '#6c757d' }},
      { name: 'blue', colors: { '--primary-color': '#007bff', '--secondary-color': '#6c757d' }},
    ]);

    onMounted(() => {
      const savedDarkMode = localStorage.getItem('darkMode');
      if (savedDarkMode !== null) {
        isDarkMode.value = savedDarkMode === 'true';
        document.documentElement.classList.toggle('dark', isDarkMode.value);
      }

      const savedTheme = localStorage.getItem('selectedTheme');
      if (savedTheme) {
        selectedTheme.value = savedTheme;
        applyTheme(savedTheme);
      }
    });

    const toggleDarkMode = () => {
      isDarkMode.value = !isDarkMode.value;
      document.documentElement.classList.toggle('dark', isDarkMode.value);
      localStorage.setItem('darkMode', isDarkMode.value);
    };

    const changeTheme = () => {
      localStorage.setItem('selectedTheme', selectedTheme.value);
      applyTheme(selectedTheme.value);
    };

    const applyTheme = (themeName) => {
      const theme = themes.value.find(t => t.name === themeName);
      if (theme) {
        Object.keys(theme.colors).forEach(color => {
          document.documentElement.style.setProperty(color, theme.colors[color]);
        });
      }
    };

    return {
      isDarkMode,
      selectedTheme,
      themes,
      toggleDarkMode,
      changeTheme,
    };
  },
  computed: {
    defaultButtonClass() {
      return 'py-2 px-4 rounded max-w-[200px] 4k:py-4 4k:px-8 4k:text-xl dark:bg-black dark:text-white bg-white text-black';
    },
  },
};
</script>

<style scoped>
/* Additional styles if needed */
</style>
