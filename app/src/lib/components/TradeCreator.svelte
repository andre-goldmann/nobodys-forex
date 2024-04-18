<script lang="ts">
    import {onMount} from "svelte";
    let symbol:string = 'EURUSD';
    let type:string = '';
    const HOST = "https://85.215.32.163";
    import {ignoredSignalsApiData, ignoredSignals, ignoredSignalSelected} from '$lib/store.ts';
    import type {IgnoredSignal} from "$lib/model";

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

    async function loadIgnoredSignals() {
        //http://85.215.32.163/ignoredsignals
        await fetch(HOST + ":6081/ignoredsignals")
            .then(response => response.json())
            .then(data => {
                //let trades:Trade[] = data;
                //let trades:IgnoredSignal[] = JSON.parse(data);
                //console.info(trades);
                //console.info("Ignored Trades:");
                //console.info(data);
                ignoredSignalsApiData.set(data);
            }).catch(error => {
                console.log(error);
                //// Just for Testing ////
                let mock:IgnoredSignal[] = [];
                let signal:IgnoredSignal = {
                    id: 1,
                    json: "{symbol:'EURUSD'}",
                    reason: "Failure whatever"
                };
                mock.push(signal);
                ignoredSignalsApiData.set(mock);
                //// Just for Testing ////
            });
    }

    function rowSelected(signal:IgnoredSignal) {
        console.info(`Call delete action on: ${signal}`);
        ignoredSignalSelected.set(signal);
    }

    onMount(() => {
        loadIgnoredSignals();
    })

    function deleteSignal(id:number) {
        console.info(`Call delete action on: ${id}`);
        /*fetch(HOST + ":6081/deleteignoredsignal/" + id)
            .then(response => response.json())
            .then(data => {
                console.info(data);
                loadIgnoredSignals();
            }).catch(error => {
            console.log(error);
        });*/
        let data = {
            id: id
        };
        fetch(HOST + ":6081/deleteignoredsignal", {
            method: 'POST',
            headers: {
                //'Access-Control-Allow-Origin': '*',
                //'Access-Control-Allow-Methods': 'DELETE, POST, GET, OPTIONS',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

    }
</script>

<div class="flex flex-row">
    <!--form class="flex items-center space-x-6" action="http://127.0.0.1:6081/createorder" on:submit|preventDefault={handleSubmit} method="POST"-->
    <!--div class="basis-1/4">

        <form class="flex items-center space-x-6" action="http://85.215.32.163:6081/createorder" on:submit|preventDefault={handleSubmit} method="POST">
            <div class="bg-transparent px-6 py-8 rounded shadow-md text-primary w-full">
                <h1 class="mb-8 text-3xl text-center">New Order</h1>
                <div class="w-full max-w-xs">
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
                        <option value="CADCHF">CADCHF</option>
                        <option value="NZDJPY">NZDJPY</option>
                    </select>
                </div>

                <div class="w-full max-w-xs">
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
    </div-->
    <div class="basis-1/4">

        <h1 class="mb-8 text-3xl text-center">Ignored Signals</h1>

        <table class="table">
            <thead>
            <tr>
                <!--th>ID</th-->
                <th>JSON</th>
                <th>REASON</th>
                <!--th></th-->
            <tr/>
            </thead>
            {#each $ignoredSignals as signal}
                <tr class="hover" on:click={() => rowSelected(signal)}>
                    <!--td>{signal.id}</td-->
                    <td>{signal.json}</td>
                    <td>{signal.reason}</td>

                    <!--button class="btn btn-ghost btn-xs" on:click={() => rowSelected(trade)}>
                        Remove
                    </button-->
                <tr/>
            {/each}
        </table>

    </div>
    {#if $ignoredSignalSelected}
        <div class="basis-1/4">
            <form class="flex items-center space-x-6" action="https://85.215.32.163/resendsignal" on:submit|preventDefault={handleSubmit} method="POST">
                <div class="bg-transparent px-6 py-8 rounded shadow-md text-primary w-full">
                    <h1 class="mb-8 text-3xl text-center">Update Signal</h1>

                    <div class="w-full">

                        <textarea class="textarea textarea-bordered"
                                id="json"
                                name="json"
                                rows="6"
                                cols="42"
                                value={$ignoredSignalSelected.json}/>
                    </div>

                    <div>
                        <button type="submit" class="btn btn-primary">Update</button>
                        <button type="button" class="btn btn-primary" on:click={() => deleteSignal($ignoredSignalSelected.id)}>Delete</button>
                    </div>

                </div>
            </form>
        </div>
    {/if}

</div>