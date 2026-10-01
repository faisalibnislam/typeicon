// Imports exactly three icons; nothing else from the 19k-module catalog
// should end up in the production bundle.
import { defineComponent, h } from 'vue';
import Home from '@typeicon/vue/line/home';
import Search from '@typeicon/vue/rounded/search';
import BrandGithub from '@typeicon/vue/brands/brand-github';

export default defineComponent({
  name: 'App',
  setup() {
    return () =>
      h('nav', { style: { display: 'flex', gap: '16px', alignItems: 'center' } }, [
        h('a', { href: '/' }, [h(Home, { size: 20 }), ' Home']),
        h('button', { type: 'button', 'aria-label': 'Search' }, [h(Search, { size: 20, strokeWidth: 1.5 })]),
        h(BrandGithub, { size: 32, color: '#2563eb', title: 'GitHub' }),
      ]);
  },
});
