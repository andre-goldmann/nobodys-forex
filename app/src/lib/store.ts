import { writable, derived } from 'svelte/store';

/** Store for your data.
 This assumes the data you're pulling back will be an array.
 If it's going to be an object, default this to an empty object.
 **/
export const symbolsApiData = writable([]);
export const tradesApiData = writable([]);
export const tradeSelected = writable();
export const ignoredSignalsApiData = writable([]);

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