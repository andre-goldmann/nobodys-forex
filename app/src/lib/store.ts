import { writable, derived } from 'svelte/store';

/** Store for your data.
 This assumes the data you're pulling back will be an array.
 If it's going to be an object, default this to an empty object.
 **/
export const symbolsApiData = writable([]);
export const tradesApiData = writable([]);
export const tradeSelected = writable();
export const ignoredSignalsApiData = writable([]);

export const ignoredSignalSelected = writable();

export const strategiesSelected = writable();
export const strategySelected = writable();

export const instrumentStatsSelected = writable();

export const executedsignalsSelected = writable();

export const trendInfoApiData = writable();


export const trendinfos = derived(trendInfoApiData, ($apiData) => {
    if ($apiData){
        //return $apiData.sort(e => e.level);
        return $apiData.sort((a,b) => (a.symbol > b.symbol) ? 1 : ((b.symbol > a.symbol) ? -1 : 0))
    }
    return [];
});


export const executedsignals = derived(executedsignalsSelected, ($apiData) => {
    if ($apiData){
        //return $apiData.sort(e => e.level);
        return $apiData.sort((a,b) => (a.closed > b.closed) ? 1 : ((b.closed > a.closed) ? -1 : 0))
    }
    return [];
});

export const instrumentStats = derived(instrumentStatsSelected, ($apiData) => {
    if ($apiData){
        //return $apiData.sort(e => e.level);
        return $apiData.sort((a,b) => (a.symbol > b.symbol) ? 1 : ((b.symbol > a.symbol) ? -1 : 0))
    }
    return [];
});

export const strategies = derived(strategiesSelected, ($apiData) => {
    if ($apiData){
        //return $apiData.sort(e => e.level);
        return $apiData.sort((a,b) => (a.profit < b.profit) ? 1 : ((b.profit < a.profit) ? -1 : 0))
    }
    return [];
});

export const symbols = derived(symbolsApiData, ($apiData) => {
    if ($apiData){
        //return $apiData.sort(e => e.level);
        return $apiData.sort((a,b) => (a.level > b.level) ? 1 : ((b.level > a.level) ? -1 : 0))
    }
    return [];
});

export const trades = derived(tradesApiData, ($apiData) => {
    if ($apiData){
        //return $apiData.sort(e => e.level);
        return $apiData.sort((a,b) => (a.id < b.id) ? 1 : ((b.id < a.id) ? -1 : 0))
    }
    return [];
});

export const ignoredSignals = derived(ignoredSignalsApiData, ($apiData) => {
    if ($apiData){
        //return $apiData.sort(e => e.level);
        return $apiData.sort((a,b) => (a.id < b.id) ? 1 : ((b.id < a.id) ? -1 : 0))
    }
    return [];
});