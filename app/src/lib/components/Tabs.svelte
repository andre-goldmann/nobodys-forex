<script>
    export let items = [];
    export let activeTabValue = 1;

    const handleClick = tabValue => () => (activeTabValue = tabValue);
</script>

<ul>
    {#each items as item}
        <a class={activeTabValue === item.value ? 'tab tab-bordered tab-active mt-12' : 'tab tab-bordered mt-12'}>
            <span on:click={handleClick(item.value)}>{item.label}</span>
        </a>
    {/each}
</ul>
{#each items as item}
    {#if activeTabValue == item.value}
        <div class="tabs">
            <svelte:component this={item.component}/>
        </div>
    {/if}
{/each}
