<script>

	import Tabs from "$lib/components/Tabs.svelte";
    import Trades from "$lib/components/Trades.svelte";
    import TradeCreator from "$lib/components/TradeCreator.svelte";
    import TradesHistory from "$lib/components/TradesHistory.svelte";
    import TrendInfo from "$lib/components/TrendInfo.svelte";

	let items = [
		{ label: "Waiting-Trades",
			value: 1,
			component: Trades
		},
		{ label: "Ignored-Signals",
			value: 2,
			component: TradeCreator
		},
        { label: "Trades-Statistiks",
            value: 3,
            component: TradesHistory
        },
        { label: "Trendinfos",
            value: 4,
            component: TrendInfo
        },
	];

</script>
<Tabs {items} />

