// Imports exactly three icons; nothing else from the 19k-module catalog
// should end up in the production bundle.
import Home from '@typeicon/react/line/home';
import Search from '@typeicon/react/rounded/search';
import BrandGithub from '@typeicon/react/brands/brand-github';

export default function App() {
  return (
    <nav style={{ display: 'flex', gap: 16, alignItems: 'center' }}>
      <a href="/">
        <Home size={20} /> Home
      </a>
      <button type="button" aria-label="Search">
        <Search size={20} strokeWidth={1.5} />
      </button>
      <BrandGithub size={32} color="#2563eb" title="GitHub" />
    </nav>
  );
}
