<script lang="ts">
    import {onMount} from "svelte";
    let symbol:string = 'EURUSD';
    let type:string = '';
    const HOST = "http://85.215.32.163";
    import {ignoredSignalsApiData, ignoredSignals} from '$lib/store.ts';

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
        await fetch(HOST + "/ignoredsignals")
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
                return [];
            });
    }

    onMount(() => {
        loadIgnoredSignals();
    })
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
                        <option value="CADCHF">CADCHF</option>
                        <option value="NZDJPY">NZDJPY</option>
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
    <div class="basis-1/4">
        <!-- http://85.215.32.163/ignoredsignals >
        TODO create a form to load and resend the ignoredSignals-->
        <p>Resend JSONS:</p>
        {#each $ignoredSignals as signal}
            {signal}
        {/each}

    </div>
</div>