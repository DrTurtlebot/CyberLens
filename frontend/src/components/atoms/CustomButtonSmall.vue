<template>
  <button
    :class="[
      ' bg-gray-200 transition-colors duration-[400ms] text-black border-2 border-gray-100 p-2 cursor-pointer inline-flex  text-sm rounded-[10px] py-[5px] px-[5px] justify-end hover:bg-gray-300 dark:bg-zinc-700 dark:text-zinc-50 dark:border-zinc-800 dark:hover:bg-zinc-800 4k:py-[8px] 4k:px-[25px] 4k:text-3xl transition-transform hover:scale-105 hover:duration-[200ms];',
      extraClasses
    ]"
    @click="handleClick"
  >
    <slot />
  </button>
</template>

<script>
export default {
  props: {
    extraClasses: {
      type: String,
      default: '',
    },
    onClick: {
      type: Function,
      default: null,
    },
  },
  methods: {
    handleClick(event) {
      if (this.onClick) {
        this.onClick(event);
      }
    },
  },
};
</script>
