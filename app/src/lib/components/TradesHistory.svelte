<script lang="ts">

    import {onMount} from "svelte";
    import type {Strategy} from "$lib/model";
    const HOST = "http://85.215.32.163:6081";
    async function loadStats(){
        await fetch(HOST + "/signalstats")
            .then(response => response.json())
            .then(data => {
                //console.info(data);
                let strategies:Strategy[] = data;
                //let strategies:Strategy[] = JSON.parse(data);
                console.info(strategies);
                //tradesApiData.set(data);
            }).catch(error => {
                console.log(error);
                //tradesApiData.set([]);
            });
    }

    onMount(() => {
        loadStats();
    });

</script>

<div>

</div>
