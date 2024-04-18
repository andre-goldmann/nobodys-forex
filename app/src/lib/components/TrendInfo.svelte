<script lang="ts">

    import {onMount} from "svelte";
    import type {TrendInfo} from "$lib/model";
    import {
        trades,
        trendInfoApiData, trendinfos
    } from "$lib/store";

    const HOST = "https://85.215.32.163:6081";

    async function loadTrendInfos(){
        await fetch(HOST + "/trendinfos")
            .then(response => response.json())
            .then(data => {
                let trendinfosData:TrendInfo[] = data;
                //console.info(strategies);
                trendInfoApiData.set(trendinfosData);
            }).catch(error => {
                console.log(error);
                trendInfoApiData.set([]);
            });
    }

    onMount(() => {
        loadTrendInfos();
    });


</script>

<div class="flex flex-row">

    <div class="w-full">
        <div class="bg-transparent px-6 py-8 rounded shadow-md text-primary w-full">
            <h1 class="mb-8 text-3xl text-center">Trendinfos</h1>

            <div class="overflow-x-auto">

                <table class="table">
                    <thead>
                    <tr>
                        <th>SYMBOL</th>
                        <th>STAMP</th>
                        <th>TRENDSCORE</th>
                        <th>UPTREND</th>
                        <th>SS</th>
                        <th>R1</th>
                    <tr/>
                    </thead>
                    {#each $trendinfos as info}
                        <tr class="hover">
                            <td>{info.symbol}</td>
                            <td>{info.stamp}</td>
                            <td>{info.trendscore}</td>
                            <td>{info.uptrend}</td>
                            <td>{info.s1}</td>
                            <td>{info.r1}</td>
                        <tr/>
                    {/each}
                </table>

            </div>

        </div>
    </div>
</div>
