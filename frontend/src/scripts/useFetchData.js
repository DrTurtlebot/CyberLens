import { ref, onMounted, watch } from 'vue';

export function useFetchData(apiEndpoint, props) {
    const loading = ref(true);
    const error = ref(null);
    const responseData = ref(null);
    const fetchData = (inputValue) => {
        loading.value = true;
        error.value = null;
        responseData.value = null;
        const viteBackendAddress = import.meta.env.VITE_BACKEND_ADDRESS || "http://localhost:4000"; // Access the environment variable here
        fetch(`${viteBackendAddress}${apiEndpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(inputValue),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                responseData.value = data;
                console.log(data);
            })
            .catch(err => {
                error.value = err.message;
            })
            .finally(() => {
                loading.value = false;
            });
    };

    // Initial fetch when component mounts
    onMounted(() => {
        fetchData(props.input);
    });

    // Watch for changes in the input prop and re-fetch data
    watch(() => props.input, (newInput) => {
        fetchData(newInput);
    });

    return {
        loading,
        error,
        responseData,
    };
}
