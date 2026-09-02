import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';

// Nettoyage automatique du DOM après chaque test
afterEach(() => {
  cleanup();
});
