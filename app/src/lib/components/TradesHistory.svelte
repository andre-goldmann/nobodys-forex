<script lang="ts">

    import {onMount} from "svelte";
    import type {Executedsignal, InstrumentStat, Strategy, Trade} from "$lib/model";
    import {
        executedsignals,
        executedsignalsSelected,
        instrumentStats,
        instrumentStatsSelected,
        strategies,
        strategiesSelected,
        strategySelected
    } from "$lib/store";
    const minSucessPercentage = 65;
    const minSucessTrades = 150;
    const allTradesPerStrategyCount = 300;
    const minProfit = 75;
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

    function loadExecutedSignals(strategy: Strategy) {
        console.info(`Load loadExecutedSignals for: ${strategy.strategy}`);
        fetch(HOST + "/executedsignals/?strategy=" + encodeURI(strategy.strategy))
            .then(response => response.json())
            .then(data => {
                let executedsignals:Executedsignal[] = data;
                //console.info(executedsignals[executedsignals.length-1]);
                executedsignalsSelected.set(executedsignals);
            }).catch(error => {
            console.log(error);
            executedsignalsSelected.set([]);
        });
    }

    function onStrategySelected(strategy:Strategy) {
        console.info(`Show details for: ${strategy.strategy}`);
        strategySelected.set(strategy);
        loadInstrumentstats(strategy);
        loadExecutedSignals(strategy);
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
        //console.info(`Load instrument stats for: ${strategy.strategy}`);
        fetch(HOST + "/instrumentstats/?strategy=" + encodeURI(strategy.strategy))
            .then(response => response.json())
            .then(data => {
                let InstrumentStatsData:InstrumentStat[] = data;
                //console.info(InstrumentStatsData);
                instrumentStatsSelected.set(InstrumentStatsData);
            }).catch(error => {
            console.log(error);
            instrumentStatsSelected.set([]);
        });
    }

    function onSelectTrade(trade:Trade) {

    }

</script>


<div class="flex h-screen bg-transparent w-full text-primary">
    <div class="flex-1 flex flex-col overflow-hidden">
        <header class="flex justify-between items-center p-4">
            <div class="flex">Strategies</div>
            <div>
                <p>Min-Win-Percentage: {minSucessPercentage}</p>
                <p>Min-Trades: {minSucessTrades}</p>
                <p>Min-Profit: {minProfit}</p>
            </div>
            <div class="flex">Instruments</div>
        </header>
        <div class="flex h-full">
            <nav class="flex w-38 h-full">
                <div class="w-full flex mx-auto px-6 py-8">
                    <div class="w-full h-full flex items-start justify-start overflow-x-auto">
                        <ul class="max-w-md divide-y divide-gray-200 dark:divide-gray-700">

                            {#each $strategies as strategy}
                                {#if strategy.tradestotal >= allTradesPerStrategyCount}
                                    <li class="pb-3 sm:pb-4 cursor-pointer" on:click={() => onStrategySelected(strategy)}>
                                        <div class="flex items-center space-x-4 rtl:space-x-reverse">
                                            <div class="flex-1 min-w-0">
                                                <p class="text-sm font-medium">
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
                                {/if}
                            {/each}

                        </ul>
                    </div>
                </div>
            </nav>
            <main class="flex flex-col w-full bg-white overflow-x-hidden overflow-y-auto mb-14">
                <div class="flex w-full mx-auto px-2 py-2">
                    <div class="flex flex-col w-full h-full text-gray-900">
                        <div class="flex w-full">
                            <h1 class=" text-3xl text-center">Strategy-Details</h1>
                            (select an instrument to see details)
                        </div>
                        {#if $strategySelected}
                            ({$strategySelected.strategy}-Instrument)
                        {:else}
                            Select a Strategy
                        {/if}


                        <!--button class="btn btn-neutral">Hello UI</button>
                        <button class="btn btn-neutral">Hello UI</button-->

                        <div class="flex flex-row">

                            <div class="w-full">
                                <div class="bg-transparent px-6 py-8 rounded shadow-md text-primary w-full">

                                    <div class="overflow-x-auto">

                                        <table class="table">
                                            <thead>
                                            <tr>
                                                <th>symbol</th>
                                                <th>Type</th>
                                                <th>Entry/Lots/Exit</th>
                                                <th>SL/TP</th>
                                                <th>Profit/Swap/Commission</th>
                                                <th>Stamp/Closed</th>
                                            <tr/>
                                            </thead>
                                            {#each $executedsignals as trade}
                                                <tr class="hover" on:click={() => onSelectTrade(trade)}>
                                                    <td>{trade.symbol}</td>
                                                    <td>{trade.type}</td>
                                                    <td>{trade.entry} <br/>{trade.lots} <br/>{trade.exit}</td>
                                                    <td>{trade.sl}<br/> {trade.tp}</td>
                                                    <td>{trade.profit}<br/> {trade.swap}<br/> {trade.commision}</td>
                                                    <td>{trade.stamp} <br/>{trade.closed}</td>

                                                <tr/>
                                            {/each}
                                        </table>

                                    </div>

                                </div>
                            </div>

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
            <nav class="flex w-38 h-full">
                <div class="w-full flex mx-auto px-6 py-8">
                    <div class="w-full h-full flex items-start justify-start overflow-x-auto">
                        <ul class="max-w-md divide-y divide-gray-200 dark:divide-gray-700">
                            {#each $instrumentStats as stat}
                                {#if stat.tradestotal > minSucessTrades}
                                    <li class="pb-3 sm:pb-4 cursor-pointer" on:click={() => onInstrumentSelected(stat)}>
                                        <!--
                                        Python:
                                        percentage = (100 / signalStats.alltrades) * signalStats.successtrades
                                        if percentage < 60:
                                        -->
                                            <div class={(100 / stat.tradestotal) * stat.tradessuccess > minSucessPercentage && stat.tradestotal >= minSucessTrades && stat.profit > minProfit ? "bg-green-400 flex items-center space-x-4 rtl:space-x-reverse": "bg-red-400 flex items-center space-x-4 rtl:space-x-reverse"}>
                                             <!--div class="flex items-center space-x-4 rtl:space-x-reverse"-->
                                              <div class="flex-1 min-w-0">
                                                  <p class="text-sm font-medium truncate text-black">
                                                      {stat.symbol}
                                                  </p>
                                                  <p class="text-sm truncate text-black w-fit">
                                                      Total: {stat.tradestotal} Win: {stat.tradessuccess} Loss: {stat.tradesfailed}
                                                  </p>
                                              </div>
                                              <div class="inline-flex items-center text-base font-semibold text-black">
                                                  <!--{roundNumber(stat.profit)} €-->
                                                  {(100 / stat.tradestotal) * stat.tradessuccess} %
                                              </div>
                                        </div>
                                    </li>
                                    {:else}
                                    <li class="pb-3 sm:pb-4 cursor-pointer" on:click={() => onInstrumentSelected(stat)}>

                                        <div class="flex items-center space-x-4 rtl:space-x-reverse">
                                            <div class="flex-1 min-w-0">
                                                <p class="text-sm font-medium truncate">
                                                    {stat.symbol}
                                                </p>
                                                <p class="text-sm truncate w-fit">
                                                    Total: {stat.tradestotal} Win: {stat.tradessuccess} Loss: {stat.tradesfailed}
                                                </p>
                                            </div>
                                            <div class="inline-flex items-center text-base font-semibold">
                                                {(100 / stat.tradestotal) * stat.tradessuccess} %
                                            </div>
                                        </div>
                                    </li>
                                {/if}

                            {/each}
                        </ul>
                    </div>
                </div>
            </nav>
        </div>
    </div>
</div>

<style>
    active{
        color: red;
    }
    inactive{
        color: green;
    }
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
