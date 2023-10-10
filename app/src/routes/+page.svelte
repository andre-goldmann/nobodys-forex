<script lang="ts">

    import SupportResistance from "$lib/components/SupportResistance.svelte";
    import Emas from "$lib/components/Emas.svelte";
    import Signals from "$lib/components/Signals.svelte";
    import Tabs from "$lib/components/Tabs.svelte";
    import '$lib/global.css';

    import { onMount } from 'svelte';
    import webSocket from '$lib/websocket';
    import {symbolsApiData} from '$lib/store.ts';
    import type {Candle, SrLevel} from "$lib/model";
    import {writable, derived} from 'svelte/store';
    import '$lib/global.css';
    let wsClient;

    const HOST = "http://85.215.32.163:6081";

    // TODO read find the biggest daily candle this is then the diff here
    let diff:number = 0.02194;

    // TODO das muss vom Server kommen
    const store = createMapStore({
        EURUSD: 1.05844,
        GBPUSD: 1.22378,
        XRPUSD: 0,
        XAGUSD: 21.590,
    });

    function createMapStore(initial) {
        const store = writable(initial);
        const set = (key, value) => store.update(m => Object.assign({}, m, {[key]: value}));
        const results = derived(store, s => ({
            keys: Object.keys(s),
            values: Object.values(s),
            entries: Object.entries(s),
            set(k, v) {
                store.update(s => Object.assign({}, s, {[k]: v}))
            },
            remove(k) {
                store.update(s => {
                    delete s[k];
                    return s;
                });
            }
        }));
        return {
            subscribe: results.subscribe,
            set: store.set,
        }
    }

    onMount(() => {
        wsClient = webSocket();

        wsClient.on('message', (event: any) => {
            let candle:Candle = JSON.parse(event.data);
            if (candle.symbol !== undefined) {
                $store.set(candle.symbol, candle.CLOSE);
            }
        });

        wsClient.on('error', (error: any) => {
            console.log('websocket error', error);
        });

        wsClient.on('open', () => {
            console.log('websocket connection established');
        });

        wsClient.on('close', () => {
            console.log('websocket connection closed');
        });
    });


    async function loadSrLevels(symbol:string){
        await fetch(HOST + "/srlevels/?symbol=" + symbol)
            .then(response => response.json())
            .then(data => {

                let filteredData:SrLevel[] = JSON.parse(data)
                    .filter((e) => e.symbol === symbol);

                var actualLevel:number = 0.0;
                $store.entries.forEach(e => {
                    if(symbol === e[0]) {
                        //console.info(e[0] + ": " + e[1]);
                        actualLevel = e[1];
                    }
                });
                if("XAGUSD" === symbol){
                    diff = 2.87
                    //console.info(filteredData);
                    //console.info(`ActualLevel: ${actualLevel}`);
                }else
                    diff =  0.02194


                let lower = actualLevel - diff;
                let upper = actualLevel + diff;

                var between:SrLevel[] = filteredData.filter(function(item) {
                    return (item.level > lower && item.level < upper);
                });
                between.forEach((entry:SrLevel) => {
                    //entry.distance = actualLevel > entry.level ?
                    entry.distance = actualLevel - entry.level;
                });

                symbolsApiData.set(between);
            }).catch(error => {
                console.log(error);
                return [];
            });
    }

    function symbolSelected(symbol:string): string{
        loadSrLevels(symbol.key);
        return "Loaded"
    }

    let items = [
        { label: "Support Resistance",
            value: 1,
            component: SupportResistance
        },
        { label: "Emas",
            value: 2,
            component: Emas
        },
        { label: "Signals",
            value: 3,
            component: Signals
        }
    ];

</script>
<div class="container mx-auto">
    {#each $store.entries as [key, value]}
        <!--div>{key}: {value}</div-->
        <div class="bg-white shadow-lg shadow-gray-200 rounded-2xl p-4 my-2"
             style="cursor: pointer; background-color: transparent;" on:click={symbolSelected({key})}>
            <div class="flex items-center">
                <div class="inline-flex flex-shrink-0 justify-center items-center w-12 h-12 text-white bg-gradient-to-br from-pink-500 to-voilet-500 rounded-lg shadow-md shadow-gray-300">
                    <i class="ni ni-money-coins text-lg" aria-hidden="true"></i>
                </div>
                <div class="flex-shrink-0 ml-3">
                    <span class="text-2xl font-bold leading-none text-primary">{value}</span>
                    <h3 class="text-base font-normal text-gray-500">{key}</h3>
                </div>
                <div class="flex flex-1 justify-end items-center ml-5 w-0 text-base font-bold text-primary">
                    +16% (TODO todays change)
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
                    </svg>
                </div>
            </div>
        </div>
        <br>
    {/each}
    <Tabs {items} />
</div>
