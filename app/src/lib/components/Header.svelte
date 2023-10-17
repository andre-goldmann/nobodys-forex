<script lang="ts">
	import { page } from '$app/stores';
	import logo from '$lib/images/svelte-logo.svg';
	import github from '$lib/images/github_white.svg';
	import "$lib/global.css";
	import {themes} from "$lib/themes/index.js";
	import {onMount} from "svelte";
	let current_theme:string = 'black';

	onMount(() => {
		if (typeof window !== 'undefined') {
			const theme = window.localStorage.getItem('theme')
			if (theme && themes.includes(theme)) {
				document.documentElement.setAttribute('data-theme', theme)
				current_theme = theme

			}
		}
	});

	function set_theme(event: Event) {
		const select = event.target as HTMLSelectElement
		const theme = select.value
		if (themes.includes(theme)) {
			const one_year = 60 * 60 * 24 * 365
			window.localStorage.setItem('theme', theme)
			document.cookie = `theme=${theme}; max-age=${one_year}; path=/; SameSite=Lax`
			document.documentElement.setAttribute('data-theme', theme)
			current_theme = theme
		}
	}

</script>

<header>
	<div class="corner">
		<a href="https://kit.svelte.dev">
			<img src={logo} alt="SvelteKit" />
		</a>
	</div>

	<nav>
		<svg viewBox="0 0 2 3" aria-hidden="true">
			<path d="M0,0 L1,2 C1.5,3 1.5,3 2,3 L2,0 Z" />
		</svg>
		<ul>
			<li aria-current={$page.url.pathname === '/' ? 'page' : undefined}>
				<a href="/">Home</a>
			</li>
			<li aria-current={$page.url.pathname === '/trades' ? 'page' : undefined}>
				<a href="/trades">Trades</a>
			</li>
			<li aria-current={$page.url.pathname === '/about' ? 'page' : undefined}>
				<a href="/about">About</a>
			</li>
			<li aria-current={$page.url.pathname === '/testing' ? 'page' : undefined}>
				<a href="/testing">Testing</a>
			</li>
			<!--li aria-current={$page.url.pathname === '/ai' ? 'page' : undefined}>
				<a href="/ai">AI</a>
			</li>
			<li aria-current={$page.url.pathname === '/trading' ? 'page' : undefined}>
				<a href="/trading">Trading</a>
			</li>
			<li aria-current={$page.url.pathname === '/motion' ? 'page' : undefined}>
				<a href="/motion">Animation</a>
			</li-->
		</ul>
		<svg viewBox="0 0 2 3" aria-hidden="true">
			<path d="M0,0 L0,3 C0.5,3 0.5,3 1,2 L2,0 Z" />
		</svg>
	</nav>

	<select
			bind:value={current_theme}
			data-choose-theme
			class="select select-primary max-w-xs"
			on:change={set_theme}
	>
		<option value="" disabled={current_theme !== ''}>
			Choose a theme
		</option>
		{#each themes as theme}
			<option value={theme} class="capitalize">{theme}</option>
		{/each}
	</select>

	<div class="corner">
		<a href="https://github.com/andre-goldmann">
			<img src={github} alt="GitHub" />
		</a>
	</div>
</header>

<style lang="scss">
	header {
		display: flex;
		justify-content: space-between;
	}

	.corner {
		width: 3em;
		height: 3em;
	}

	.corner a {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100%;
	}

	.corner img {
		width: 2em;
		height: 2em;
		object-fit: contain;
	}

	nav {
		display: flex;
		justify-content: center;
		--background: rgba(255, 255, 255, 0.7);
	}

	svg {
		width: 2em;
		height: 3em;
		display: block;
	}

	path {
		fill: var(--background);
	}

	ul {
		position: relative;
		padding: 0;
		margin: 0;
		height: 3em;
		display: flex;
		justify-content: center;
		align-items: center;
		list-style: none;
		background: var(--background);
		background-size: contain;
	}

	li {
		position: relative;
		height: 100%;
	}

	li[aria-current='page']::before {
		--size: 6px;
		content: '';
		width: 0;
		height: 0;
		position: absolute;
		top: 0;
		left: calc(50% - var(--size));
		border: var(--size) solid transparent;
		border-top: var(--size) solid var(--color-theme-1);
	}

	nav a {
		display: flex;
		height: 100%;
		align-items: center;
		padding: 0 0.5rem;
		color: var(--color-text);
		font-weight: 700;
		font-size: 0.8rem;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		text-decoration: none;
		transition: color 0.2s linear;
	}

	a:hover {
		color: var(--color-theme-1);
	}
</style>

