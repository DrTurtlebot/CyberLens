<template>
    <div>
        <b class="text-2xl 4k:text-5xl">Not Recognised</b>
        <div class="CardData">
            <b class="text-lg 4k:text-4xl">Sorry... But this input was not recognised as an IP Address / Domain / URL or Hash</b>
            <p><b>Tips:</b> If a Url is Https:// only and does not support http://, make sure to include it in the address</p>
        </div>  
    </div>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'AbuseIPDB',
    props: {
        input: {
            type: String,
            required: true,
        },
    },
});
</script>
