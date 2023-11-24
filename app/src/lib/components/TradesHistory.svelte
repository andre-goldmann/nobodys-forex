<script lang="ts">

    import {onMount} from "svelte";
    import type {InstrumentStat, Strategy} from "$lib/model";
    import {
        instrumentStats,
        instrumentStatsSelected,
        strategies,
        strategiesSelected,
        strategySelected
    } from "$lib/store";

    const HOST = "http://85.215.32.163:6081";
    async function loadStats(){
        await fetch(HOST + "/strategystats")
            .then(response => response.json())
            .then(data => {
                let strategies:Strategy[] = data;
                //console.info(strategies);
                strategiesSelected.set(strategies);
            }).catch(error => {
                console.log(error);
                strategiesSelected.set([]);
            });
    }

    onMount(() => {
        loadStats();
    });

    function onStrategySelected(strategy:Strategy) {
        console.info(`Show details for: ${strategy.strategy}`);
        strategySelected.set(strategy);
        loadInstrumentstats(strategy);
    }

    function onInstrumentSelected(stat:InstrumentStat) {
        console.info(`Show details for: ${stat.symbol}`);
        //strategySelected.set(strategy);
        //loadInstrumentstats(strategy);
    }

    function roundNumber(num:number) {
        return Math.round((num + Number.EPSILON) * 100) / 100;
    }

    function loadInstrumentstats(strategy:Strategy) {
        console.info(`Load instrument stats for: ${strategy.strategy}`);
        fetch(HOST + "/instrumentstats/?strategy=" + strategy.strategy)
            .then(response => response.json())
            .then(data => {
                let InstrumentStatsData:InstrumentStat[] = data;
                console.info(InstrumentStatsData);
                instrumentStatsSelected.set(InstrumentStatsData);
            }).catch(error => {
            console.log(error);
            instrumentStatsSelected.set([]);
        });
    }

</script>


<div class="flex h-screen bg-transparent w-full text-primary">
    <div class="flex-1 flex flex-col overflow-hidden">
        <header class="flex justify-between items-center p-4">
            <div class="flex">Strategies</div>
            <div class="flex">Instruments</div>
        </header>
        <div class="flex h-full">
            <nav class="flex w-38 h-full">
                <div class="w-full flex mx-auto px-6 py-8">
                    <div class="w-full h-full flex items-start justify-start">
                        <ul class="max-w-md divide-y divide-gray-200 dark:divide-gray-700">

                            {#each $strategies as strategy}
                                <li class="pb-3 sm:pb-4 cursor-pointer" on:click={() => onStrategySelected(strategy)}>
                                    <div class="flex items-center space-x-4 rtl:space-x-reverse">
                                        <div class="flex-1 min-w-0">
                                            <p class="text-sm font-medium ">
                                                {strategy.strategy}
                                            </p>
                                            <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                                                Total: {strategy.tradestotal} Win: {strategy.tradessuccess} Loss: {strategy.tradesfailed}
                                            </p>
                                        </div>
                                        <div class="inline-flex items-center text-base font-semibold dark:text-white">
                                            {roundNumber(strategy.profit)} €
                                        </div>
                                    </div>
                                </li>
                            {/each}

                        </ul>
                    </div>
                </div>
            </nav>
            <main class="flex flex-col w-full bg-white overflow-x-hidden overflow-y-auto mb-14">
                <div class="flex w-full mx-auto px-2 py-2">
                    <div class="flex flex-col w-full h-full text-gray-900">
                        <div class="flex w-full">
                            {#if $strategySelected}
                                <h3>{$strategySelected.strategy}-Instrument</h3>
                            {:else}
                                <h3>Select a Strategy</h3>
                            {/if}

                            <!--button class="btn btn-neutral">Hello UI</button>
                            <button class="btn btn-neutral">Hello UI</button-->
                        </div>
                        <!--div class="flex w-full max-w-xl h-60 items-center justify-center mx-auto bg-green-400 border-b border-gray-600">

                            <button class="btn btn-neutral">Hello UI</button>

                        </div>
                        <div class="flex w-full max-w-xl h-60 items-center justify-center mx-auto bg-green-400 border-b border-gray-600">Post</div>
                        <div class="flex w-full max-w-xl h-60 items-center justify-center mx-auto bg-green-400 border-b border-gray-600">Post</div>
                        <div class="flex w-full max-w-xl h-60 items-center justify-center mx-auto bg-green-400 border-b border-gray-600">Post</div>
                        <div class="flex w-full max-w-xl h-60 items-center justify-center mx-auto bg-green-400 border-b border-gray-600">Post</div-->
                    </div>
                </div>
            </main>
            <nav class="flex w-38 h-full bg-transparent">
                <div class="w-full flex mx-auto px-6 py-8">
                    <div class="w-full h-full flex items-start justify-start">
                        <ul class="max-w-md divide-y divide-gray-200 dark:divide-gray-700">
                            {#each $instrumentStats as stat}
                                <li class="pb-3 sm:pb-4 cursor-pointer" on:click={() => onInstrumentSelected(stat)}>
                                    <div class="flex items-center space-x-4 rtl:space-x-reverse">
                                        <div class="flex-1 min-w-0">
                                            <p class="text-sm font-medium truncate dark:text-white">
                                                {stat.symbol}
                                            </p>
                                            <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                                                Total: {stat.tradestotal} Win: {stat.tradessuccess} Loss: {stat.tradesfailed}
                                            </p>
                                        </div>
                                        <div class="inline-flex items-center text-base font-semibold dark:text-white">
                                            {roundNumber(stat.profit)} €
                                        </div>
                                    </div>
                                </li>
                            {/each}
                        </ul>
                    </div>
                </div>
            </nav>
        </div>
    </div>
</div>

<style>
    ::-webkit-scrollbar {
        width: 5px;
        height: 5px;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(13deg, #7bcfeb 14%, #e685d3 64%);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(13deg, #c7ceff 14%, #f9d4ff 64%);
    }
    ::-webkit-scrollbar-track {
        background: #ffffff;
        border-radius: 10px;
        box-shadow: inset 7px 10px 12px #f0f0f0;
    }
</style>
