import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';

// Sample test to ensure testing infrastructure works
describe('Testing Infrastructure', () => {
  test('renders without crashing', () => {
    render(<div data-testid="test-element">Test</div>);
    expect(screen.getByTestId('test-element')).toBeInTheDocument();
  });

  test('basic assertion test', () => {
    expect(true).toBe(true);
    expect('ProjectMeats3').toContain('Meats');
  });
});

// Example component test
describe('Component Testing Example', () => {
  test('should render basic component', () => {
    const TestComponent = () => <h1>Welcome to ProjectMeats3</h1>;
    render(<TestComponent />);
    expect(screen.getByText('Welcome to ProjectMeats3')).toBeInTheDocument();
  });
});