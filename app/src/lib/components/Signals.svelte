<script lang="ts">
    let symbol:string = 'EURUSD';
    let type:string = '';

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
</script>
<div class="flex flex-row">

        <div class="basis-1/4">
            <!--form class="flex items-center space-x-6" action="http://127.0.0.1:6081/createorder" on:submit|preventDefault={handleSubmit} method="POST"-->
            <form class="flex items-center space-x-6" action="https://backend.nobodys-forex.duckdns.org/createorder" on:submit|preventDefault={handleSubmit} method="POST">
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
                <h1 class="mb-8 text-3xl text-center">Running Orders</h1>

                <div class="overflow-x-auto">
                    <table class="table">
                        <!-- head -->
                        <thead>
                        <tr>
                            <th>Symbol</th>
                            <th>Entry</th>
                            <th>Stopp Loss</th>
                            <th>Take profit</th>
                            <th>Spread</th>
                            <th>Date</th>
                        </tr>
                        </thead>
                        <tbody>
                        <!-- row 1 -->
                        <tr>
                            <th>EURUSD</th>
                            <td>1.0489</td>
                            <td>1.0489</td>
                            <td>1.0489</td>
                            <td>0.01</td>
                            <td>04.10.2023 10:00:00</td>
                        </tr>

                        </tbody>
                    </table>
                </div>

            </div>
        </div>

</div>