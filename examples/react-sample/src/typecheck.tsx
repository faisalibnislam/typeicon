// Type-level tests for the generated .d.ts files. `tsc --noEmit` must pass;
// every @ts-expect-error line must actually be an error, otherwise tsc fails
// with "Unused '@ts-expect-error' directive" (proving types are not `any`).
import { useRef } from 'react';
import { createIcon } from '@typeicon/react';
import type { FilledIconComponent, IconNode, StrokeIconComponent, StrokeIconProps } from '@typeicon/react';
import Home from '@typeicon/react/line/home';
import HomeFilled from '@typeicon/react/filled/home';
import BrandGithub from '@typeicon/react/brands/brand-github';
import SearchRounded from '@typeicon/react/rounded/search';

const strokeIcon: StrokeIconComponent = Home;
const filledIcon: FilledIconComponent = BrandGithub;
const node: IconNode = [['path', { d: 'M0 0h24v24H0z' }]];
const Custom = createIcon('custom', node, { viewBox: '0 0 24 24', fill: 'currentColor' });
const props: StrokeIconProps = { size: '1.5em', color: 'red', title: 'Home', strokeWidth: 1.5 };

export function TypeTests() {
  const ref = useRef<SVGSVGElement>(null);
  return (
    <>
      <Home size={32} color="red" strokeWidth={1.5} className="x" title="Home" ref={ref} />
      <Home size="2em" aria-label="Home" onClick={(e) => e.currentTarget.getBBox()} {...props} />
      <HomeFilled size={16} style={{ verticalAlign: 'middle' }} />
      <BrandGithub size={24} />
      <SearchRounded strokeWidth="1.25" />
      <Custom size={12} />
      {/* @ts-expect-error size must be a number or string */}
      <Home size={true} />
      {/* @ts-expect-error filled icons are not stroke-based: no strokeWidth prop */}
      <BrandGithub strokeWidth={2} />
      {/* @ts-expect-error title must be a string */}
      <SearchRounded title={42} />
      {/* @ts-expect-error ref must target an SVGSVGElement */}
      <Home ref={useRef<HTMLDivElement>(null)} />
      {String(strokeIcon.displayName)}
      {String(filledIcon.displayName)}
    </>
  );
}
