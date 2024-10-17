<template>
    <div
      class="ModuleBox p-2 m-auto mt-0 border-2 border-solid dark:border-zinc-700 inline-block rounded-lg flex-grow max-w-4xl bg-zinc-50 dark:bg-zinc-900 4k:p-10 4k:max-w-6xl 4k:mt-4 transition-colors duration-400 animate-fadeInNoDelay "
    >
      <div class="ModuleBox-header flex justify-end items-center gap-0 mb-1 4k:gap-2 4k:mb-3">
        <!-- Add Export as PNG button -->
        <CustomButtonSmall @click="exportAsPng">
          Export PNG
        </CustomButtonSmall>
        <!-- Add Export as Black and White PNG button -->
        <CustomButtonSmall @click="exportAsBlackAndWhite">
          (B/W)
        </CustomButtonSmall>
      </div>
      <div class="ModuleBox__content 4k:scale-105" ref="content">
        <slot></slot>
      </div>
    </div>
  </template>
  
  
  <script>
  import { toPng } from 'html-to-image';
  import CustomButtonSmall from '@atoms/CustomButtonSmall.vue';
  
  export default {
    name: 'ModuleBox',
    data() {
      return {
        copied: false,
      };
    },
    components: {
      CustomButtonSmall,
    },
    methods: {
      copyContent() {
        const content = this.$refs.content;
        const range = document.createRange();
        range.selectNode(content);
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(range);
        document.execCommand('copy');
        window.getSelection().removeAllRanges();
        this.copied = true;
        setTimeout(() => {
          this.copied = false;
        }, 1500);
      },
      async exportAsPng() {
        try {
          const content = this.$refs.content;
          if (!content) {
            console.error('Content not found!');
            return;
          }
  
          const isDarkMode = document.documentElement.classList.contains('dark');
          const backgroundColor = isDarkMode ? '#18181b' : '#fafafa';
  
          const dataUrl = await toPng(content, {
            cacheBust: true,
            quality: 1,
            backgroundColor: backgroundColor,
          });
  
          const link = document.createElement('a');
          link.href = dataUrl;
          link.download = 'module-content.png';
          link.click();
        } catch (error) {
          console.error('Error exporting as PNG:', error);
        }
      },
      async exportAsBlackAndWhite() {
        try {
          const content = this.$refs.content;
          if (!content) {
            console.error('Content not found!');
            return;
          }
  
          const isDarkMode = document.documentElement.classList.contains('dark');
          const backgroundColor = isDarkMode ? '#18181b' : '#fafafa';
  
          // Temporarily apply grayscale filter
          content.style.filter = 'grayscale(100%)';
  
          // Convert the content to a PNG
          const dataUrl = await toPng(content, {
            cacheBust: true,
            quality: 1,
            backgroundColor: backgroundColor,
          });
  
          // Remove the grayscale filter immediately after capture
          content.style.filter = '';
  
          const link = document.createElement('a');
          link.href = dataUrl;
          link.download = 'module-content-black-and-white.png';
          link.click();
        } catch (error) {
          console.error('Error exporting as Black and White PNG:', error);
        }
      },
    },
  };
  </script>
  