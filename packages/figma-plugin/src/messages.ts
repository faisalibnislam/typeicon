// Message shapes exchanged between the UI iframe and the main thread.
// The main thread still validates everything it receives at runtime
// (see validateInsertMessage in shared.ts); these types are for authoring.

import type { IconStyle } from './shared';

export type UiToMain =
  | { type: 'get-settings' }
  | { type: 'set-settings'; apiBase: string }
  | {
      type: 'insert';
      svg: string;
      name: string;
      style: IconStyle;
      source: string;
      license: string;
      id: string;
      color: string | null;
    }
  | { type: 'close' };

export type MainToUi =
  | { type: 'settings'; apiBase: string; defaultApiBase: string }
  | { type: 'settings-error'; error: string }
  | { type: 'inserted'; name: string }
  | { type: 'insert-error'; error: string };
