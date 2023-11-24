<script lang="ts">
	import Counter from './Counter.svelte';
	import welcome from '$lib/images/svelte-welcome.webp';
	import welcome_fallback from '$lib/images/svelte-welcome.png';
</script>

<!--svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head-->


<!-- component -->
<div class="flex h-screen bg-green-300">
	<div class="flex-1 flex flex-col overflow-hidden">
		<header class="flex justify-between items-center bg-blue-300 p-4">
			<div class="flex">Strategies</div>
			<div class="flex">Instruments</div>
		</header>
		<div class="flex h-full">
			<nav class="flex w-38 h-full bg-pink-500">
				<div class="w-full flex mx-auto px-6 py-8">
					<div class="w-full h-full flex items-start justify-start">
						<ul class="max-w-md divide-y divide-gray-200 dark:divide-gray-700">
							<li class="pb-3 sm:pb-4">
								<div class="flex items-center space-x-4 rtl:space-x-reverse">
									<!--div class="flex-shrink-0">
										<img class="w-8 h-8 rounded-full" src="/docs/images/people/profile-picture-1.jpg" alt="Neil image">
									</div-->
									<div class="flex-1 min-w-0">
										<p class="text-sm font-medium text-gray-900 truncate dark:text-white">
											NNR
										</p>
										<p class="text-sm text-gray-500 truncate dark:text-gray-400">
											Total: 96 Win: 64 Loss: 32
										</p>
									</div>
									<div class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
										35%
									</div>
								</div>
							</li>
							<li class="pb-3 sm:pb-4">
								<div class="flex items-center space-x-4 rtl:space-x-reverse">
									<!--div class="flex-shrink-0">
										<img class="w-8 h-8 rounded-full" src="/docs/images/people/profile-picture-1.jpg" alt="Neil image">
									</div-->
									<div class="flex-1 min-w-0">
										<p class="text-sm font-medium text-gray-900 truncate dark:text-white">
											Super AI Trend
										</p>
										<p class="text-sm text-gray-500 truncate dark:text-gray-400">
											email@flowbite.com
										</p>
									</div>
									<div class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
										54%
									</div>
								</div>
							</li>
							<li class="py-3 sm:py-4">
								<div class="flex items-center space-x-4 rtl:space-x-reverse">
									<!--div class="flex-shrink-0">
										<img class="w-8 h-8 rounded-full" src="/docs/images/people/profile-picture-3.jpg" alt="Neil image">
									</div-->
									<div class="flex-1 min-w-0">
										<p class="text-sm font-medium text-gray-900 truncate dark:text-white">
											AI Volume Supertrend
										</p>
										<p class="text-sm text-gray-500 truncate dark:text-gray-400">
											email@flowbite.com
										</p>
									</div>
									<div class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
										65%
									</div>
								</div>
							</li>
							<li class="py-3 sm:py-4">
								<div class="flex items-center space-x-4 rtl:space-x-reverse">
									<!--div class="flex-shrink-0">
										<img class="w-8 h-8 rounded-full" src="/docs/images/people/profile-picture-2.jpg" alt="Neil image">
									</div-->
									<div class="flex-1 min-w-0">
										<p class="text-sm font-medium text-gray-900 truncate dark:text-white">
											SSL Hybrid
										</p>
										<p class="text-sm text-gray-500 truncate dark:text-gray-400">
											email@flowbite.com
										</p>
									</div>
									<div class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
										06560
									</div>
								</div>
							</li>
							<li class="py-3 sm:py-4">
								<div class="flex items-center space-x-4 rtl:space-x-reverse">
									<!--div class="flex-shrink-0">
										<img class="w-8 h-8 rounded-full" src="/docs/images/people/profile-picture-5.jpg" alt="Neil image">
									</div-->
									<div class="flex-1 min-w-0">
										<p class="text-sm font-medium text-gray-900 truncate dark:text-white">
											Thomas Lean
										</p>
										<p class="text-sm text-gray-500 truncate dark:text-gray-400">
											email@flowbite.com
										</p>
									</div>
									<div class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
										$2367
									</div>
								</div>
							</li>
							<li class="pt-3 pb-0 sm:pt-4">
								<div class="flex items-center space-x-4 rtl:space-x-reverse">
									<!--div class="flex-shrink-0">
										<img class="w-8 h-8 rounded-full" src="/docs/images/people/profile-picture-4.jpg" alt="Neil image">
									</div-->
									<div class="flex-1 min-w-0">
										<p class="text-sm font-medium text-gray-900 truncate dark:text-white">
											Lana Byrd
										</p>
										<p class="text-sm text-gray-500 truncate dark:text-gray-400">
											email@flowbite.com
										</p>
									</div>
									<div class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
										$367
									</div>
								</div>
							</li>
						</ul>
					</div>
				</div>
			</nav>
			<main class="flex flex-col w-full bg-white overflow-x-hidden overflow-y-auto mb-14">
				<div class="flex w-full mx-auto px-2 py-2">
					<div class="flex flex-col w-full h-full text-gray-900">
						<div class="flex w-full">
							<h3>Strategy-Instrument</h3>
							<button class="btn btn-neutral">Hello UI</button>
							<button class="btn btn-neutral">Hello UI</button>
						</div>
						<!--div class="flex w-full max-w-xl h-60 items-center justify-center mx-auto bg-green-400 border-b border-gray-600">

							<button class="btn btn-neutral">Hello UI</button>

						</div>
						<div class="flex w-full max-w-xl h-60 items-center justify-center mx-auto bg-green-400 border-b border-gray-600">Post</div>
						<div class="flex w-full max-w-xl h-60 items-center justify-center mx-auto bg-green-400 border-b border-gray-600">Post</div>
						<div class="flex w-full max-w-xl h-60 items-center justify-center mx-auto bg-green-400 border-b border-gray-600">Post</div>
						<div class="flex w-full max-w-xl h-60 items-center justify-center mx-auto bg-green-400 border-b border-gray-600">Post</div-->
					</div>
				</div>
			</main>
			<nav class="flex w-38 h-full bg-yellow-400">
				<div class="w-full flex mx-auto px-6 py-8">
					<div class="w-full h-full flex items-start justify-start">

						<ul class="max-w-md divide-y divide-gray-200 dark:divide-gray-700">
							<li class="pb-3 sm:pb-4">
								<div class="flex items-center space-x-4 rtl:space-x-reverse">
									<!--div class="flex-shrink-0">
										<img class="w-8 h-8 rounded-full" src="/docs/images/people/profile-picture-1.jpg" alt="Neil image">
									</div-->
									<div class="flex-1 min-w-0">
										<p class="text-sm font-medium text-gray-900 truncate dark:text-white">
											AUDCHF
										</p>
										<p class="text-sm text-gray-500 truncate dark:text-gray-400">
											Total: 96 Win: 64 Loss: 32
										</p>
									</div>
									<div class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
										85%
									</div>
								</div>
							</li>
							<li class="py-3 sm:py-4">
								<div class="flex items-center space-x-4 rtl:space-x-reverse">
									<!--div class="flex-shrink-0">
										<img class="w-8 h-8 rounded-full" src="/docs/images/people/profile-picture-3.jpg" alt="Neil image">
									</div-->
									<div class="flex-1 min-w-0">
										<p class="text-sm font-medium text-gray-900 truncate dark:text-white">
											AUDNZD
										</p>
										<p class="text-sm text-gray-500 truncate dark:text-gray-400">
											email@flowbite.com
										</p>
									</div>
									<div class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
										1.0849
									</div>
								</div>
							</li>
							<li class="py-3 sm:py-4">
								<div class="flex items-center space-x-4 rtl:space-x-reverse">
									<!--div class="flex-shrink-0">
										<img class="w-8 h-8 rounded-full" src="/docs/images/people/profile-picture-2.jpg" alt="Neil image">
									</div-->
									<div class="flex-1 min-w-0">
										<p class="text-sm font-medium text-gray-900 truncate dark:text-white">
											AUDUSD
										</p>
										<p class="text-sm text-gray-500 truncate dark:text-gray-400">
											email@flowbite.com
										</p>
									</div>
									<div class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
										06560
									</div>
								</div>
							</li>
							<li class="py-3 sm:py-4">
								<div class="flex items-center space-x-4 rtl:space-x-reverse">
									<!--div class="flex-shrink-0">
										<img class="w-8 h-8 rounded-full" src="/docs/images/people/profile-picture-5.jpg" alt="Neil image">
									</div-->
									<div class="flex-1 min-w-0">
										<p class="text-sm font-medium text-gray-900 truncate dark:text-white">
											Thomas Lean
										</p>
										<p class="text-sm text-gray-500 truncate dark:text-gray-400">
											email@flowbite.com
										</p>
									</div>
									<div class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
										$2367
									</div>
								</div>
							</li>
							<li class="pt-3 pb-0 sm:pt-4">
								<div class="flex items-center space-x-4 rtl:space-x-reverse">
									<!--div class="flex-shrink-0">
										<img class="w-8 h-8 rounded-full" src="/docs/images/people/profile-picture-4.jpg" alt="Neil image">
									</div-->
									<div class="flex-1 min-w-0">
										<p class="text-sm font-medium text-gray-900 truncate dark:text-white">
											Lana Byrd
										</p>
										<p class="text-sm text-gray-500 truncate dark:text-gray-400">
											email@flowbite.com
										</p>
									</div>
									<div class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
										$367
									</div>
								</div>
							</li>
						</ul>
					</div>
				</div>
			</nav>
		</div>
	</div>
</div>

<style>
	::-webkit-scrollbar {
		width: 5px;
		height: 5px;
	}
	::-webkit-scrollbar-thumb {
		background: linear-gradient(13deg, #7bcfeb 14%, #e685d3 64%);
		border-radius: 10px;
	}
	::-webkit-scrollbar-thumb:hover {
		background: linear-gradient(13deg, #c7ceff 14%, #f9d4ff 64%);
	}
	::-webkit-scrollbar-track {
		background: #ffffff;
		border-radius: 10px;
		box-shadow: inset 7px 10px 12px #f0f0f0;
	}
</style>
