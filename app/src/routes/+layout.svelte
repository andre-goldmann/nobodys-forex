<script lang="ts">
    // Import our global CSS
    import "$lib/global.css";
    import Header from "$lib/components/Header.svelte";
</script>

<div class="app">

    <Header />

    <main class="px-8">
        <slot />
    </main>

</div>

<style>
    .app {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }
</style>