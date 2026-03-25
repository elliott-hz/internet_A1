import { useState } from 'react';
import { useCartOperations } from './useCart';

/**
 * Custom hook for generic API calls
 * Provides reusable API call logic with loading and error states
 */
export const useApi = (apiFunction) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = async (...args) => {
    setLoading(true);
    try {
      const result = await apiFunction(...args);
      setData(result);
      setError(null);
      return result;
    } catch (err) {
      setError(err.message || 'API call failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setData(null);
    setError(null);
    setLoading(false);
  };

  return {
    data,
    loading,
    error,
    execute,
    reset,
  };
};

// Re-export cart hook for convenience
export { useCartOperations as useCart };
