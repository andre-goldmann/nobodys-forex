import { writable, derived } from 'svelte/store';

/** Store for your data.
 This assumes the data you're pulling back will be an array.
 If it's going to be an object, default this to an empty object.
 **/
export const apiData = writable([]);

export const symbols = derived(apiData, ($apiData) => {
    if ($apiData){
        //return $apiData.sort(e => e.level);
        return $apiData.sort((a,b) => (a.level > b.level) ? 1 : ((b.level > a.level) ? -1 : 0))
    }
    return [];
});