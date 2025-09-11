// Test setup for ProjectMeats3 Frontend
import '@testing-library/jest-dom';

// Mock environment variables
process.env.NODE_ENV = 'test';
process.env.REACT_APP_API_URL = 'http://localhost:8000';

// Global test utilities and mocks
global.console = {
  ...console,
  // Suppress console.log/warn/error in tests unless needed
  log: jest.fn(),
  warn: jest.fn(),
  error: jest.fn(),
};

// Mock fetch for API calls
global.fetch = jest.fn();

beforeEach(() => {
  jest.clearAllMocks();
});

// Custom render function for testing (you can extend this)
export * from '@testing-library/react';
export { default as userEvent } from '@testing-library/user-event';