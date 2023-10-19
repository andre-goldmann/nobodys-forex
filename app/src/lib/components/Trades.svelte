<script lang="ts">
    import type {Trade} from "$lib/model";
    import {onMount} from "svelte";
    const HOST = "http://85.215.32.163:6081";
    import {tradesApiData, tradeSelected} from '$lib/store.ts';
    import {trades} from "$lib/store";

    const handleSubmit = e => {
        // getting the action url
        const ACTION_URL = e.target.action

        // get the form fields data and convert it to URLSearchParams
        const formData = new FormData(e.target)

        fetch(ACTION_URL, {
            method: 'POST',
            body: formData
        });
    }

    async function loadUnActiveTrades(){
        await fetch(HOST + "/unActiveTrades")
            .then(response => response.json())
            .then(data => {
                //let trades:Trade[] = data;
                //let trades:Trade[] = JSON.parse(data);
                //console.info(trades);
                tradesApiData.set(data);
            }).catch(error => {
                console.log(error);
                tradesApiData.set([]);
            });
    }

    onMount(() => {
        loadUnActiveTrades();
    });

    function rowSelected(trade:Trade) {
        console.info(`Call delete action on: ${trade}`);
        tradeSelected.set(trade);
    }

</script>
<div class="flex flex-row">

        <div class="w-full">
            <div class="bg-transparent px-6 py-8 rounded shadow-md text-primary w-full">
                <h1 class="mb-8 text-3xl text-center">Inactive Orders</h1>

                <div class="overflow-x-auto">

                    <table class="table">
                        <thead>
                        <tr>
                            <th>ID</th>
                            <th>SYMBOL</th>
                            <th>TYPE</th>
                            <th>ENTRY</th>
                            <th>SL</th>
                            <th>TP</th>
                            <th>LOTS</th>
                            <th>STAMP</th>
                            <!--th></th-->
                        <tr/>
                        </thead>
                        {#each $trades as trade}
                            <tr class="hover" on:click={() => rowSelected(trade)}>
                                <td>{trade.id}</td>
                                <td>{trade.symbol}</td>
                                <td>{trade.type}</td>
                                <td>{trade.entry}</td>
                                <td>{trade.sl}</td>
                                <td>{trade.tp}</td>
                                <td>{trade.lots}</td>
                                <td>{trade.stamp}</td>
                                <!--button class="btn btn-ghost btn-xs" on:click={() => rowSelected(trade)}>
                                    Remove
                                </button-->
                            <tr/>
                        {/each}
                    </table>

                </div>

            </div>
        </div>

    {#if $tradeSelected}
        <div class="basis-1/4">
            <!--form class="flex items-center space-x-6" action="http://127.0.0.1:6081/createorder" on:submit|preventDefault={handleSubmit} method="POST"-->
            <form class="flex items-center space-x-6" action="http://85.215.32.163:6081/modifyorder" on:submit|preventDefault={handleSubmit} method="POST">
                <div class="bg-transparent px-6 py-8 rounded shadow-md text-primary w-full">
                    <h1 class="mb-8 text-3xl text-center">Update Order</h1>

                    <div class="w-full max-w-xs">
                        <!--label class="label" for="symbols">
                            <span class="label-text">Symbol</span>
                        </label-->
                        <input
                                type="number"
                                class="input input-bordered input-primary w-full max-w-xs mb-4"
                                id="id"
                                name="id"
                                value={$tradeSelected.id}
                                readonly/>
                    </div>

                    <div class="w-full max-w-xs">
                        <!--label class="label" for="symbols">
                            <span class="label-text">Symbol</span>
                        </label-->
                        <input
                                type="text"
                                class="input input-bordered input-primary w-full max-w-xs mb-4"
                                id="symbol"
                                name="symbol"
                                value={$tradeSelected.symbol}
                                readonly/>
                    </div>

                    <div class="w-full max-w-xs">

                        <input
                                type="text"
                                class="input input-bordered input-primary w-full max-w-xs mb-4"
                                id="type"
                                name="type"
                                value={$tradeSelected.type}
                                readonly/>
                    </div>

                    <input
                            type="number"
                            step=".0001"
                            class="input input-bordered input-primary w-full max-w-xs mb-4"
                            id="entry"
                            name="entry"
                            value={$tradeSelected.entry}
                            placeholder="Entry" />

                    <input
                            type="number"
                            step=".0001"
                            class="input input-bordered input-primary w-full max-w-xs mb-4"
                            id="sl"
                            name="sl"
                            value={$tradeSelected.sl}
                            placeholder="Stoploss" />

                    <input
                            type="number"
                            step=".0001"
                            class="input input-bordered input-primary w-full max-w-xs mb-4"
                            id="tp"
                            name="tp"
                            value={$tradeSelected.tp}
                            placeholder="Take Profit" />
                    <input
                            type="number"
                            step=".001"
                            class="input input-bordered input-primary w-full max-w-xs mb-4"
                            id="lots"
                            name="lots"
                            value={$tradeSelected.lots}
                            placeholder="Volume/Lots" />

                    <div>
                        <button type="submit" class="btn btn-primary">Update</button>
                        <button type="button" class="btn btn-primary">Delete</button>
                    </div>

                </div>
            </form>
        </div>
    {/if}
</div>