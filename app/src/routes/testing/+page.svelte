<script>

	// List of tab items with labels, values and assigned components
	import Tab1 from "$lib/components/Tab1.svelte";
	import Tab2 from "$lib/components/Tab2.svelte";
	import Tab3 from "$lib/components/Tab3.svelte";
	import Tabs from "$lib/components/Tabs.svelte";

	let items = [
		{ label: "Content",
			value: 1,
			component: Tab1
		},
		{ label: "Interactions",
			value: 2,
			component: Tab2
		},
		{ label: "Tab 3",
			value: 3,
			component: Tab3
		}
	];
</script>

<Tabs {items} />