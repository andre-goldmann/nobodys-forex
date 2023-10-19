<script>

	import Tabs from "$lib/components/Tabs.svelte";
    import Trades from "$lib/components/Trades.svelte";
    import TradeCreator from "$lib/components/TradeCreator.svelte";
    import TradesHistory from "$lib/components/TradesHistory.svelte";

	let items = [
		{ label: "Active-Trades",
			value: 1,
			component: Trades
		},
		{ label: "Trade Action",
			value: 2,
			component: TradeCreator
		},
        { label: "Trades-History",
            value: 3,
            component: TradesHistory
        },
	];

</script>
<Tabs {items} />

