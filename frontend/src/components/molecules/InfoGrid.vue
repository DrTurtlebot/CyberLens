<template>
  <div class="grid grid-cols-[minmax(0,auto),1fr] gap-x-5 gap-y-2 items-center p-2 m-auto min-w-[340px] 4k:min-w-[680px] max-w-[600px] 4k:gap-x-8 4k:gap-y-4 4k:max-w-[1200px] 4k:p-4">
    <!-- Loop over infoItems, with optional color for value -->
    <div v-for="(item, index) in infoItems" :key="index" class="contents">
      <!-- Label in the first column -->
      <div class="text-left font-bold max-w-[400px] min-w-[100px] justify-self-start 4k:text-3xl 4k:max-w-[800px] 4k:min-w-[200px]">
        <b>{{ item.label }}</b>
      </div>
      <!-- Value in the second column with dynamic color classes -->
      <div
        :class="[
          'text-right max-w-[250px] break-words justify-self-end 4k:text-3xl 4k:max-w-[500px]',
          item.color ? item.color : ''
        ]"
      >
        <p>{{ item.value }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InfoGrid',
  props: {
    infoItems: {
      type: Array,
      required: true,
    },
  },
};
</script>
