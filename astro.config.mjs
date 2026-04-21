// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	site: 'https://example.com',
	integrations: [
		starlight({
			title: 'Ultimate CSS Web Design',
			description: '上級者向け CSS / Web Design 教本。原典を再編し、実務補足と参考実装を強化。',
			sidebar: [
				{
					label: '導入',
					items: [
						{ label: 'トップ', slug: '' },
					],
				},
				{
					label: '設計基盤',
					items: [
						{ label: 'Terminology', slug: 'references/terminology' },
						{ label: 'Foundation', slug: 'references/foundation' },
						{ label: 'Responsive', slug: 'references/responsive' },
						{ label: 'Tokens', slug: 'references/tokens' },
						{ label: 'Spacing', slug: 'references/spacing' },
						{ label: 'Color', slug: 'references/color' },
						{ label: 'Z-Index', slug: 'references/z-index' },
						{ label: 'Typography', slug: 'references/typography' },
						{ label: 'Accessibility', slug: 'references/accessibility' },
					],
				},
				{
					label: 'モーションと表現',
					items: [
						{ label: 'Animations', slug: 'references/animations' },
						{ label: 'Keyframes', slug: 'references/keyframes' },
						{ label: 'Visual Details', slug: 'references/visual-details' },
					],
				},
			],
		}),
	],
});
