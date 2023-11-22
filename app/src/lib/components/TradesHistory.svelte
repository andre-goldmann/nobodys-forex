<script lang="ts">

    import {onMount} from "svelte";
    import type {Strategy} from "$lib/model";
    import {strategies, strategiesSelected} from "$lib/store";
    let color = '#ff3e00';

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

    function rowSelected(strategy:Strategy) {
        console.info(`Show details for: ${strategy}`);
        //strategiesSelected.set(strategy);
    }

</script>

<div class="flex flex-row">

    <div class="w-full">
        <div class="bg-transparent px-6 py-8 rounded shadow-md text-primary w-full">
            <h1 class="mb-8 text-3xl text-center">Strategy-Details</h1>

            <div class="overflow-x-auto">

                <table class="table">
                    <thead>
                    <tr>
                        <th>Strategy</th>
                        <th>Trades Total</th>
                        <th>Trades Failed</th>
                        <th>Trades Success</th>
                        <th>Profit</th>
                        <th>Swap</th>
                        <th>Commission</th>
                        <!--th></th-->
                    <tr/>
                    </thead>
                    {#each $strategies as strategy}
                        <tr class="hover" on:click={() => rowSelected(strategy)}>
                            <td>{strategy.strategy}</td>
                            <td>{strategy.tradestotal}</td>
                            <td>{strategy.tradesfailed}</td>
                            <td>{strategy.tradessuccess}</td>
                            <td>{strategy.profit}</td>
                            <td>{strategy.swap}</td>
                            <td>{strategy.commission}</td>

                            <!--button class="btn btn-ghost btn-xs" on:click={() => rowSelected(trade)}>
                                Remove
                            </button-->
                        <tr/>
                    {/each}
                </table>

            </div>

        </div>
    </div>

</div>
