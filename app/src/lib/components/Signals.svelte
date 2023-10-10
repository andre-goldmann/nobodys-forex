<script lang="ts">
    import type {Trade} from "$lib/model";
    import {onMount} from "svelte";
    let symbol:string = 'EURUSD';
    let type:string = '';
    const HOST = "http://85.215.32.163:6081";
    import {symbols, tradesApiData} from '$lib/store.ts';
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
                return [];
            });
    }

    onMount(() => {
        loadUnActiveTrades();
    });

    function deleteRow(id:number) {
        console.info(`Call delete action on: ${id}`);

    }

</script>
<div class="flex flex-row">

        <div class="basis-1/4">
            <!--form class="flex items-center space-x-6" action="http://127.0.0.1:6081/createorder" on:submit|preventDefault={handleSubmit} method="POST"-->
            <form class="flex items-center space-x-6" action="http://85.215.32.163:6081/createorder" on:submit|preventDefault={handleSubmit} method="POST">
                <div class="bg-transparent px-6 py-8 rounded shadow-md text-primary w-full">
                    <h1 class="mb-8 text-3xl text-center">New Order</h1>
                    <div class="w-full max-w-xs">
                        <!--label class="label" for="symbols">
                            <span class="label-text">Symbol</span>
                        </label-->
                        <select class="select select-primary w-full max-w-xs mb-4"
                                id="symbol"
                                name="symbol"
                                bind:value={symbol}>
                            <option selected>Choose a Symbol</option>
                            <option value="EURUSD">EURUSD</option>
                            <option value="GBPUSD">GBPUSD</option>
                            <option value="XRPUSD">XRPUSD</option>
                            <option value="XAGUSD">XAGUSD</option>
                            <option value="USDCHF">USDCHF</option>
                            <option value="GBPJPY">GBPJPY</option>
                            <option value="EURJPY">EURJPY</option>
                            <option value="AUDNZD">AUDNZD</option>
                            <option value="USDCAD">USDCAD</option>
                            <option value="EURNZD">EURNZD</option>
                            <option value="GBPNZD">GBPNZD</option>
                            <option value="NZDUSD">NZDUSD</option>
                            <option value="EURGBP">EURGBP</option>
                            <option value="USDJPY">USDJPY</option>
                            <option value="AUDJPY">AUDJPY</option>
                            <option value="GBPCHF">GBPCHF</option>
                            <option value="EURCHF">EURCHF</option>
                            <option value="CHFJPY">CHFJPY</option>
                        </select>
                    </div>

                    <div class="w-full max-w-xs">
                        <!--label class="label" for="symbols">
                            <span class="label-text">Symbol</span>
                        </label-->
                        <select class="select select-primary w-full max-w-xs mb-4"
                                id="type"
                                name="type"
                                bind:value={type}>
                            <option selected>Choose a Type</option>
                            <option value="buy">Buy</option>
                            <option value="sell">Sell</option>
                        </select>
                    </div>

                    <input
                            type="number"
                            step=".0001"
                            class="input input-bordered input-primary w-full max-w-xs mb-4"
                            id="entry"
                            name="entry"
                            placeholder="Entry" />

                    <input
                            type="number"
                            step=".0001"
                            class="input input-bordered input-primary w-full max-w-xs mb-4"
                            id="sl"
                            name="sl"
                            placeholder="Stoploss" />

                    <input
                            type="number"
                            step=".0001"
                            class="input input-bordered input-primary w-full max-w-xs mb-4"
                            id="tp"
                            name="tp"
                            placeholder="Take Profit" />
                    <input
                            type="number"
                            step=".001"
                            class="input input-bordered input-primary w-full max-w-xs mb-4"
                            id="lots"
                            name="lots"
                            value="0.01"
                            placeholder="Volume/Lots" />

                    <button type="submit" class="btn btn-primary">Submit</button>

                </div>
            </form>
        </div>


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
                            <th></th>
                        <tr/>
                        </thead>
                        {#each $trades as trade}
                            <tr class="hover">
                                <td>{trade.id}</td>
                                <td>{trade.symbol}</td>
                                <td>{trade.type}</td>
                                <td>{trade.entry}</td>
                                <td>{trade.sl}</td>
                                <td>{trade.tp}</td>
                                <td>{trade.lots}</td>
                                <button class="btn btn-ghost btn-xs" on:click={() => deleteRow(trade.id)}>
                                    Remove
                                </button>
                            <tr/>
                        {/each}
                    </table>


                </div>

            </div>
        </div>

</div>