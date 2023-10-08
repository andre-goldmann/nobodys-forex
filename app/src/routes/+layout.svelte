<script lang="ts">
    // Import our global CSS
    import "$lib/global.css";
    import Header from "$lib/components/Header.svelte";
</script>

<div class="app">

    <Header />

    <main class="container mx-auto">
        <slot />
    </main>

</div>