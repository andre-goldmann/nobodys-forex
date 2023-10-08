<script lang="ts">
    import {symbols} from "$lib/store";

    /*function filter(){
        console.info("Filter ...");
        console.info("Symbol: " + symbol);
        console.info("Calculator: " + calculator);
        console.info("Type: " + type);
        console.info("Diff: " + diff);
        console.info($store);

    }*/
</script>

<!-- Das muss hier bleiben sonst werden die Symbol-Cards nicht untereinander angezeigt -->
<div class="container mx-auto">

    <!--button on:click={clearActualLevels}>Clear</button>
    <p>Signals:</p>
    {#each actualLevels as signal, i}
        <li>{signal.symbol} {signal.DATE} {signal.TIME} {signal.CLOSE}</li>
    {/each}-->

    <!--button on:click={() => $store.set('EURUSD', 4)} class="btn-primary">Set c to 4</button-->

    <div class="grid grid-cols-2 gap-4">

        <div>
            <!--div>
                <div class="w-full max-w-xs">
                    <label class="label" for="diff">
                        <span class="label-text">DIFF</span>
                    </label>
                    <input class="input select-primary w-full max-w-xs"
                           id="diff"
                           type="number"
                           name="diff"
                           placeholder="Type your diff (0.01, 0.02 etc.) here"
                           bind:value={diff}>
                </div>

            </div-->
        </div>
        <div>
            <!--div style="margin-top: 38px">
                <button on:click={filter}
                        class="btn btn-neutral" type="submit">
                    Filter
                </button>
            </div-->
        </div>

        <div>
            <!--div class="w-full max-w-xs">
                <label class="label" for="type">
                    <span class="label-text">TYPE</span>
                </label>
                <select class="select select-primary w-full max-w-xs"
                        id="symbols"
                        name="symbols"
                        bind:value={type}>
                    <option selected>Choose a Type</option>
                    <option value="SUPPORT">Support</option>
                    <option value="RESISTANCE">Resistance</option>
                    <option value="BOTH">Both</option>
                </select>
            </div-->
        </div>
        <div>
            <!-- Keep me -->
        </div>
        <div>
            <!--div class="w-full max-w-xs">
                <label class="label" for="caclulator">
                    <span class="label-text">Caclulator</span>
                </label>
                <select class="select select-primary w-full max-w-xs"
                        id="symbols"
                        name="symbols"
                        bind:value={calculator}>
                    <option selected>Choose a Type</option>
                    <option value="defaultsr">Default Support Resistance</option>
                    <option value="trendlinebreakout">Trendline Breakout</option>
                    <option value="All">All</option>
                </select>
            </div-->
        </div>

        <div class="col-span-2">

            <div class="overflow-x-auto">
                <table class="table">
                    <thead>
                    <tr>
                        <th>LEVEL</th>
                        <th>DISTANCE</th>
                        <th>TYPE</th>
                        <th>CALCULATOR</th>
                    <tr/>
                    </thead>
                    {#each $symbols as drinkName}
                        <tr class="hover">
                            <td>{drinkName.level}</td>
                            <td>{drinkName.distance}</td>
                            <td>{drinkName.type === 0 ? 'SUPPORT' : 'RESISTANCE'}</td>
                            <td>{drinkName.caclulator}</td>
                        <tr/>
                    {/each}
                </table>
            </div>

        </div>
    </div>
</div>