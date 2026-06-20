import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import App from '../App';

// Mock Recharts to avoid jsdom layout/dimensions exceptions
vi.mock('recharts', () => ({
  ResponsiveContainer: ({ children }: any) => <div data-testid="responsive-container">{children}</div>,
  PieChart: ({ children }: any) => <div data-testid="pie-chart">{children}</div>,
  Pie: () => null,
  Cell: () => null,
}));

describe('Syntho Frontend App Component', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('renders simulated Telegram login widget on startup', () => {
    render(<App />);
    expect(screen.getByText('Syntho')).toBeInTheDocument();
    expect(screen.getByText(/Self-hosted AI-powered Notes & Expense Assistant/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Masuk dengan Telegram/i })).toBeInTheDocument();
  });

  it('navigates to dashboard overview when login is clicked', () => {
    render(<App />);
    
    const loginButton = screen.getByRole('button', { name: /Masuk dengan Telegram/i });
    fireEvent.click(loginButton);

    // Verify it transitions to the dashboard by checking for overview dashboard text
    expect(screen.getByRole('heading', { name: 'Overview' })).toBeInTheDocument();
    expect(screen.getByText(/Saldo Bersih/i)).toBeInTheDocument();
    expect(screen.getByText(/Total Pemasukan/i)).toBeInTheDocument();
    expect(screen.getByText(/Total Pengeluaran/i)).toBeInTheDocument();
  });
});
