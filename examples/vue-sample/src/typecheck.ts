// Type-level tests for the generated .d.ts files. `tsc --noEmit` must pass;
// every @ts-expect-error line must actually be an error.
import { defineComponent, h } from 'vue';
import { createIcon } from '@typeicon/vue';
import type { IconComponent, IconNode, IconProps } from '@typeicon/vue';
import Home from '@typeicon/vue/line/home';
import BrandGithub from '@typeicon/vue/brands/brand-github';
import SearchRounded from '@typeicon/vue/rounded/search';

const icon: IconComponent = Home;
const node: IconNode = [['path', { d: 'M0 0h24v24H0z' }]];
const Custom: IconComponent = createIcon('custom', node, { viewBox: '0 0 24 24', fill: 'currentColor' });
const props: IconProps = { size: '1.5em', color: 'red', title: 'Home', strokeWidth: 1.5 };

export const TypeTests = defineComponent({
  components: { Home, BrandGithub, SearchRounded, Custom },
  setup() {
    return () => [
      h(Home, { size: 32, color: 'red', strokeWidth: 1.5, title: 'Home' }),
      h(Home, props),
      h(BrandGithub, { size: '2em' }),
      h(SearchRounded, { strokeWidth: '1.25', class: 'x', 'aria-label': 'Home' }),
      h(icon),
      // @ts-expect-error size must be a number or string
      h(Home, { size: true }),
      // @ts-expect-error title must be a string
      h(SearchRounded, { title: 42 }),
    ];
  },
});
