<script>

	import Tabs from "$lib/components/Tabs.svelte";
    import Trades from "$lib/components/Trades.svelte";
    import TradeCreator from "$lib/components/TradeCreator.svelte";

	let items = [
		{ label: "Trades-Overview",
			value: 1,
			component: Trades
		},
		{ label: "Trade",
			value: 2,
			component: TradeCreator
		}
	];


</script>
<Tabs {items} />

